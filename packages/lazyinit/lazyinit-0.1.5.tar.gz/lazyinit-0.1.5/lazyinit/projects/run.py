import lazydl as l
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from omegaconf import DictConfig
import hydra
import datetime
import pandas as pd
from tqdm import tqdm
import traceback


l.hi()
log = l.Logger(__name__)
current_dir = os.path.dirname(os.path.abspath (__file__))


@hydra.main(version_base="1.2", config_path="configs/", config_name="default_config.yaml")
def main(config: DictConfig) -> float:
    experiment = None
    try:
        exp_start = datetime.datetime.now()
        config, experiment = l.init_env(config=config, current_dir=current_dir)
        
        if experiment:
            experiment.log_other("Task Status", "Pending")
        
        # ---------------------------------------------------------------------------- #
        #                         排队                                     
        # ---------------------------------------------------------------------------- #
        config = l.set_processing_units(config)
        
        
        if experiment:
            experiment.log_other("Task Status", "Running")
        
        
        # ---------------------------------------------------------------------------- #
        #                         加载模型                                     
        # ---------------------------------------------------------------------------- #
        model, tokenizer = l.load_model_and_tokenizer(config.model_name_or_path, use_qlora=config.use_qlora, backbone_file=config.get("backbone_file", None), params=config)
        
        pre_end = datetime.datetime.now()
        
        if config.stage != "test":
            # ---------------------------------------------------------------------------- #
            #                            初始化Trainer                                  
            # ---------------------------------------------------------------------------- #
            if config.trainer_type == 'hf':
                trainer = l.HFTrainer(
                    model=model,
                    args=config.hf_args,
                    train_dataset=l.load_data(config, tokenizer, stage="train", return_dataloader=False),
                    compute_loss=config.loss_func_file
                )
                
            elif config.trainer_type == 'lit':
                trainer = l.LitTrainer(config,
                                        model=l.load_class(config.lit_model_file)(config, tokenizer, model=model), 
                                        tokenizer=tokenizer,
                                        train_dataloader=l.load_data(config, tokenizer, stage="train"),
                                        val_dataloader=l.load_data(config, tokenizer, stage="val"),
                                        experiment=experiment,)

                
            else:
                raise ValueError("Unknown trainer type: %s" % config.trainer_type)
            
            
            trainer.train()


            # ---------------------------------------------------------------------------- #
            #                         结果保存                                     
            # ---------------------------------------------------------------------------- #
            if config.use_qlora:
                final_save_path = os.path.join(config.output_dir, 'lora_weights')
            else:
                final_save_path = os.path.join(config.output_dir, 'best')
            trainer.save_model(final_save_path)

            if config.use_qlora and config.merge_lora:
                log.info("Merge lora weights to base model!")
                model = l.merge_lora_to_base_model(config.model_name_or_path, final_save_path, config.output_dir + "/best")
            else:
                model = trainer.model.backbone
        
        
        eval_result_str = ""
        
        if config.test_data_file and config.test_data_file != "":
            # ---------------------------------------------------------------------------- #
            #                         测试模型                                     
            # ---------------------------------------------------------------------------- #
            test_dataset = l.load_data(config, tokenizer, stage="test", return_dataloader=False)
            prompt = l.load_class(config.prompt_file)(tokenizer)
            eval_pipline = l.Pipeline(model, tokenizer, user_role_code=prompt.user_role_code, bot_role_code=prompt.bot_role_code)
            
            def iterate_data(data, step=1, desc=""):
                for r in tqdm([data[i:i + step] for i in range(0, len(data), step)], desc=desc):
                    yield r
            
            
            model_responses = []
            for batch in iterate_data(test_dataset, step=8, desc="模型正在生成回复"):
                try:
                    model_response = eval_pipline.generate(**batch)
                except Exception as e:
                    log.warning("生成回复时出现错误: %s" % e)
                    log.warning(traceback.format_exc())
                    model_response = [""] * len(batch)
                model_responses.extend(model_response)
            
            test_dataset = test_dataset.add_column("model_responses", model_responses)

            
            result= l.get_eval_metrics(test_dataset, config.eval_metrics)
            eval_result_str = result.flatten_to_print()
            
            test_dataset.to_csv(config.output_dir + "/test_generate.csv")
            
            if experiment:
                log.info("上传测评结果至 Comet.ml ！")
                experiment.log_others(result)
                experiment.log_table(tabular_data=pd.DataFrame(test_dataset), filename="test_gererate" + ".csv")
            
            l.save_as(result, config.output_dir + "/test_result.json", data_name="评测结果")
        
        redis_client = l.RedisClient()
        redis_client.deregister_gpus(config.task_id)
        redis_client.deregister_process(config.task_id)
        
        if experiment:
            experiment.log_other("Task Status", "End")
        
        train_or_test_end = datetime.datetime.now()
        
        pre_time_day = int((pre_end - exp_start).total_seconds() // 60 // 60 // 24)
        pre_time_hour = int((pre_end - exp_start).total_seconds() // 60 // 60)
        pre_time_minute = int((pre_end - exp_start).total_seconds() // 60 % 60)
        
        run_time_day = int((train_or_test_end - pre_end).total_seconds() // 60 // 60 // 24)
        run_time_hour = int((train_or_test_end - pre_end).total_seconds() // 60 // 60)
        run_time_minute = int((train_or_test_end - pre_end).total_seconds() // 60 % 60)
    
        
        if config.dingding_access_token and config.dingding_secret:
            end_notice = (
                f"{config.task_id} 任务已完成\n"
                f"实验名称：{config.comet_exp_name}\n"
                f"实验备注：{config.memo}\n"
                f"实验准备总耗时：{pre_time_day} 天 {pre_time_hour} 小时 {pre_time_minute} 分钟\n"
                f"实验运行总耗时：{run_time_day} 天 {run_time_hour} 小时 {run_time_minute} 分钟\n\n"
                f"{eval_result_str}\n"
            )
            l.notice(end_notice)
    
    except Exception as e:
        error_file = str(e.__traceback__.tb_frame.f_globals["__file__"])
        error_line = str(e.__traceback__.tb_lineno)
        traceback_error = traceback.format_exc()
        error_notice = (
            f"{config.task_id} 任务失败\n"
            f"实验名称：{config.comet_exp_name}\n"
            f"实验备注：{config.memo}\n"
            f"异常信息：{e}\n"
            f"发生异常的文件：{error_file}\n"
            f"发生异常的行数：{error_line}\n"
            f"异常详情：{traceback_error}\n"
        )
        if experiment:
            experiment.log_other("Task Status", "Error")
        l.notice(error_notice)
    
if __name__ == "__main__":
    main()
