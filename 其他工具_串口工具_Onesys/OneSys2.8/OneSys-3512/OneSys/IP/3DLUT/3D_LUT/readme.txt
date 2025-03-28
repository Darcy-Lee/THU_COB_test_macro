lut3d_model instructions：

//0 pre train
lut3d_model.exe -i 0 -pf lut3d_measure_sample_preTrain.csv
//1 train and test
lut3d_model.exe -i 1 -f lut3d_measure_sample_train.csv -t lut3d_target_data.csv

其中，-i 表示模式选择，0代表进行预训练，1代表进行训练和使用。

// 附加条件，需要预训练样本（lut3d_measure_sample_preTrain.csv）、训练样本（lut3d_measure_sample_train.csv）、以及测试样本（lut3d_target_data.csv，Gen3DLUT.exe -Gamut 0 -MOD 0）

