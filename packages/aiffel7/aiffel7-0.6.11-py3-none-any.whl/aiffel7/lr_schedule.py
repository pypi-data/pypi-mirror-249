from tensorflow.keras.optimizers.schedules import LearningRateSchedule

def lr_schedule(epoch):
    initial_lr = 0.0001  # 초기 러닝 레이트
    if epoch < 10:
        return initial_lr
    elif epoch < 20:
        return initial_lr * 0.1  # 10 에포크 후 러닝 레이트 감소
    else:
        return initial_lr * 0.01  # 20 에포크 후 러닝 레이트 추가 감소
