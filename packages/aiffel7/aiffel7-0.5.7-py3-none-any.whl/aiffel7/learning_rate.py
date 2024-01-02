from tensorflow.keras.optimizers.schedules import LearningRateSchedule

def lr_schedule(epoch, initial_lr=0.0001, decay_epochs=[10, 20], decay_rate=0.1):
    """
    Learning Rate Scheduler 함수
    
    Args:
        epoch (int): 현재 에포크 번호
        initial_lr (float): 초기 러닝 레이트
        decay_epochs (list): 러닝 레이트를 감소시킬 에포크 번호들의 리스트
        decay_rate (float): 러닝 레이트 감소 비율
        
    Returns:
        float: 현재 에포크에서의 러닝 레이트
    """
    lr = initial_lr
    for decay_epoch in decay_epochs:
        if epoch >= decay_epoch:
            lr *= decay_rate
    return lr
