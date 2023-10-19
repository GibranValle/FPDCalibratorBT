from computer_vision.ComputerVision import ComputerVision

if __name__ == "__main__":
    cv = ComputerVision()
    print(f'mu: '+cv.get_mu_status())
    print(f'mcu: '+cv.get_mcu_status())
    print(f'ff: '+cv.get_ff_status())
