import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


# errorLeft = leftSensorInput - 50
# errorRight = rightSensorInput + 50



def control (leftSensorReading1, rightSensorReading1):
    
    if leftSensorReading1>190:
        leftSensorReading1=190
    if rightSensorReading1>190:
        rightSensorReading1=190
        
        
    leftSensorReading = leftSensorReading1-50
    rightSensorReading = rightSensorReading1-50
    diff = leftSensorReading - rightSensorReading

    # Inputs
    left_sensor_D2 = np.arange(-50, 151.01, 0.01)
    right_sensor_D1 = np.arange(-50, 151.01, 0.01)
    difference = np.arange(-40, 41.01, 0.01)

    # Outputs
    left_motors = np.arange(-10, 11.01, 0.01)   # pwm increase for left motors
    right_motors = np.arange(-10, 11.01, 0.01)

    # Fuzzy membership functions for left_sensor_D2
    LNE = fuzz.trapmf(left_sensor_D2, [-50, -50, -30, -5])      # large negative distance error
    SNE = fuzz.trimf(left_sensor_D2, [-15, 0, 2])               # small negative distance error
    SPE = fuzz.trimf(left_sensor_D2, [0, 2, 15])                # small positive distance error
    MPE = fuzz.trimf(left_sensor_D2, [5, 25, 45])               # medium positive distance error
    LPE = fuzz.trapmf(left_sensor_D2, [30, 60, 150, 150])       # large positive distance error

    # Fuzzy membership functions for distance_error_right
    # for the ranges I did it such that LN (large negative distance for left) is LP2 (large positive distance for right
    # need to check MFs ranges
    LNE2 = fuzz.trapmf(right_sensor_D1, [-50, -50, -30, -5])         # large negative distance error
    SNE2 = fuzz.trimf(right_sensor_D1, [-15, 0, 2])                 # small negative distance error
    SPE2 = fuzz.trimf(right_sensor_D1, [0, 2, 15])                  # small positive distance error
    MPE2 = fuzz.trimf(right_sensor_D1, [5, 25, 45])                 # medium positive distance error
    LPE2 = fuzz.trapmf(right_sensor_D1, [30, 60, 150, 150])        # large positive distance error

    # Fuzzy membership functions for difference
    # need to check MFs ranges
    NE = fuzz.trapmf(difference, [-40, -40, -5, 0])      # negative difference
    ZE = fuzz.trimf(difference, [-0.5, 0, 0.5])      # zero difference
    PE = fuzz.trapmf(difference, [0.5, 5, 40, 40])      # positive difference

    # Fuzzy membership functions for left_motors
    LLD = fuzz.trapmf(left_motors, [-10, -10, -8, -5.6])
    SLLD = fuzz.trimf(left_motors, [-8, -5.6, -3.25])
    SLD = fuzz.trimf(left_motors, [-5, -3.25, -0.5])
    SSLD = fuzz.trimf(left_motors, [-2, 0, 0.75])
    SSLI = fuzz.trimf(left_motors, [-0.75, 0, 2])
    SLI = fuzz.trimf(left_motors, [0.5, 2.5, 4])
    SMLI = fuzz.trimf(left_motors, [2.5, 4.25, 6])
    MLI = fuzz.trimf(left_motors, [4.25, 6.2, 8])
    SLLI = fuzz.trimf(left_motors, [6.2, 7.6, 9])
    LLI = fuzz.trapmf(left_motors, [7.6, 9, 10, 10])

    # Fuzzy membership functions for right_motors
    LRD = fuzz.trapmf(right_motors, [-10, -10, -8, -5.6])
    SLRD = fuzz.trimf(right_motors, [-8, -5.6, -3.25])
    SRD = fuzz.trimf(right_motors, [-5, -3.25, -0.5])
    SSRD = fuzz.trimf(right_motors, [-2, 0, 0.75])
    SSRI = fuzz.trimf(right_motors, [-0.75, 0, 2])
    SRI = fuzz.trimf(right_motors, [0.5, 2.5, 4])
    SMRI = fuzz.trimf(right_motors, [2.5, 4.25, 6])
    MRI = fuzz.trimf(right_motors, [4.25, 6.2, 8])
    SLRI = fuzz.trimf(right_motors, [6.2, 7.6, 9])
    LRI = fuzz.trapmf(right_motors, [7.6, 9, 10, 10])


    # Activating the membership functions
    left_LNE = fuzz.interp_membership(left_sensor_D2, LNE, leftSensorReading)
    left_SNE = fuzz.interp_membership(left_sensor_D2, SNE, leftSensorReading)
    left_SPE = fuzz.interp_membership(left_sensor_D2, SPE, leftSensorReading)
    left_MPE = fuzz.interp_membership(left_sensor_D2, MPE, leftSensorReading)
    left_LPE = fuzz.interp_membership(left_sensor_D2, LPE, leftSensorReading)

    right_LNE = fuzz.interp_membership(right_sensor_D1, LNE2, rightSensorReading)
    right_SNE = fuzz.interp_membership(right_sensor_D1, SNE2, rightSensorReading)
    right_SPE = fuzz.interp_membership(right_sensor_D1, SPE2, rightSensorReading)
    right_MPE = fuzz.interp_membership(right_sensor_D1, MPE2, rightSensorReading)
    right_LPE = fuzz.interp_membership(right_sensor_D1, LPE2, rightSensorReading)

    difference_NE = fuzz.interp_membership(difference, NE, diff)
    difference_ZE = fuzz.interp_membership(difference, ZE, diff)
    difference_PE = fuzz.interp_membership(difference, PE, diff)

    # Applying rules
    # Right Motor PWM Increase

    right_LRD0 = np.fmin(np.fmin(right_LNE, left_LNE), difference_ZE)
    right_LRD1 = np.fmin(np.fmin(right_LNE, left_LNE), difference_NE)
    right_LRD2 = np.fmax(right_LRD0, right_LRD1)
    right_LRD3 = np.fmin(np.fmin(right_LNE, left_SNE), difference_PE)
    right_LRD4 = np.fmax(right_LRD2, right_LRD3)
    right_LRD5 = np.fmin(np.fmin(right_LNE, left_LPE), difference_PE)
    right_LRD6 = np.fmax(right_LRD4, right_LRD5)
    right_LRD7 = np.fmin(np.fmin(right_LNE, left_MPE), difference_PE)
    right_LRD8 = np.fmax(right_LRD6, right_LRD7)
    right_LRD9 = np.fmin(np.fmin(right_LNE, left_SPE), difference_PE)
    right_LRD = np.fmax(right_LRD8, right_LRD9)
    right_LRD = np.fmin(right_LRD, LRD)  # if error set this to max

    right_SLRD = np.fmin(np.fmin(np.fmin(right_LNE, left_LNE), difference_PE), SLRD)
    right_SRD = np.fmin(np.fmax(np.fmin(np.fmin(right_SNE, left_SPE), difference_PE),
                                np.fmax(np.fmin(np.fmin(right_SNE, left_MPE), difference_PE),
                                        np.fmax(np.fmin(np.fmin(right_SNE, left_LPE), difference_PE),
                                                np.fmax(np.fmin(np.fmin(right_SNE, left_SNE), difference_NE),
                                                        np.fmax(np.fmin(np.fmin(right_SNE, left_LNE), difference_NE),
                                                                np.fmin(np.fmin(right_SNE, left_SNE), difference_ZE)))))),
                        SRD)
    right_SSRD = np.fmin(np.fmin(np.fmin(right_SNE, left_SNE), difference_PE), SSRD)
    right_SSRI = np.fmin(np.fmax(np.fmin(np.fmin(right_SPE, left_SPE), difference_PE),
                                 np.fmin(np.fmin(right_SPE, left_MPE), difference_PE)), SSRI)
    right_SRI = np.fmin(np.fmax(np.fmin(np.fmin(right_SPE, left_LPE), difference_PE),
                                np.fmax(np.fmin(np.fmin(right_SPE, left_SPE), difference_NE),
                                        np.fmin(np.fmin(right_SPE, left_SPE), difference_ZE))), SRI)
    right_SMRI = np.fmin(np.fmin(np.fmin(right_MPE, left_MPE), difference_PE), SMRI)
    right_MRI = np.fmin(np.fmax(np.fmin(np.fmin(right_MPE, left_LPE), difference_PE),
                                np.fmax(np.fmin(np.fmin(right_MPE, left_SPE), difference_NE),
                                        np.fmax(np.fmin(np.fmin(right_MPE, left_MPE), difference_NE),
                                                np.fmax(np.fmin(np.fmin(right_MPE, left_SNE), difference_NE),
                                                        np.fmax(np.fmin(np.fmin(right_MPE, left_LNE), difference_NE),
                                                                np.fmin(np.fmin(right_MPE, left_MPE), difference_ZE)))))),
                        MRI)
    right_SLRI = np.fmin(np.fmin(np.fmin(right_LPE, left_LPE), difference_PE), SLRI)
    right_LRI = np.fmin(np.fmax(np.fmin(np.fmin(right_LPE, left_SPE), difference_NE),
                                np.fmax(np.fmin(np.fmin(right_LPE, left_MPE), difference_NE),
                                        np.fmax(np.fmin(np.fmin(right_LPE, left_LPE), difference_NE),
                                                np.fmax(np.fmin(np.fmin(right_LPE, left_SNE), difference_NE),
                                                        np.fmax(np.fmin(np.fmin(right_LPE, left_LNE), difference_NE),
                                                                np.fmin(np.fmin(right_LPE, left_LPE), difference_ZE)))))),
                        LRI)

    # Left Motor PWM Increase
    left_LLD = np.fmin(np.fmax(np.fmin(np.fmin(right_LNE, left_LNE), difference_PE),
                               np.fmax(np.fmin(np.fmin(right_LPE, left_SNE), difference_NE),
                                       np.fmax(np.fmin(np.fmin(right_MPE, left_LNE), difference_NE),
                                               np.fmax(np.fmin(np.fmin(right_LPE, left_LNE), difference_NE),
                                                       np.fmax(np.fmin(np.fmin(right_SNE, left_LNE), difference_NE),
                                                               np.fmin(np.fmin(right_LNE, left_LNE), difference_ZE)))))),
                       LLD)
    left_SLLD = np.fmin(np.fmin(np.fmin(right_LNE, left_LNE), difference_NE), SSLD)
    left_SLD = np.fmin(np.fmax(np.fmin(np.fmin(right_SNE, left_SNE), difference_PE),
                               np.fmax(np.fmin(np.fmin(right_LNE, left_SNE), difference_PE),
                                       np.fmax(np.fmin(np.fmin(right_MPE, left_SNE), difference_NE),
                                               np.fmin(np.fmin(right_SNE, left_SNE), difference_ZE)))), SLD)
    left_SSLD = np.fmin(np.fmin(np.fmin(right_SNE, left_SNE), difference_NE), SSLD)
    left_SSLI = np.fmin(np.fmin(np.fmin(right_SPE, left_SPE), difference_NE), SSLI)
    left_SLI = np.fmin(np.fmax(np.fmin(np.fmin(right_SPE, left_SPE), difference_PE),
                               np.fmax(np.fmin(np.fmin(right_SNE, left_SPE), difference_PE),
                                       np.fmax(np.fmin(np.fmin(right_LNE, left_SPE), difference_PE),
                                               np.fmax(np.fmin(np.fmin(right_MPE, left_SPE), difference_NE),
                                                       np.fmax(np.fmin(np.fmin(right_LPE, left_SPE), difference_NE),
                                                               np.fmin(np.fmin(right_SPE, left_SPE), difference_ZE)))))),
                       SLI)
    left_SMLI = np.fmin(np.fmin(np.fmin(right_MPE, left_MPE), difference_NE), SMLI)
    left_MLI = np.fmin(np.fmax(np.fmin(np.fmin(right_SPE, left_MPE), difference_PE),
                               np.fmax(np.fmin(np.fmin(right_MPE, left_MPE), difference_PE),
                                       np.fmax(np.fmin(np.fmin(right_SNE, left_MPE), difference_PE),
                                               np.fmax(np.fmin(np.fmin(right_LNE, left_MPE), difference_PE),
                                                       np.fmin(np.fmin(np.fmin(right_LPE, left_MPE), difference_NE),
                                                               np.fmin(np.fmin(right_MPE, left_MPE), difference_ZE)))))),
                       MLI)
    left_SLLI = np.fmin(np.fmin(np.fmin(right_LPE, left_LPE), difference_NE), SLLI)
    left_LLI = np.fmin(np.fmax(np.fmin(np.fmin(right_SPE, left_LPE), difference_PE),
                               np.fmax(np.fmin(np.fmin(right_MPE, left_LPE), difference_PE),
                                       np.fmax(np.fmin(np.fmin(right_LPE, left_LPE), difference_PE),
                                               np.fmax(np.fmin(np.fmin(right_SNE, left_LPE), difference_PE),
                                                       np.fmax(np.fmin(np.fmin(right_LNE, left_LPE), difference_PE),
                                                               np.fmin(np.fmin(right_LPE, left_LPE), difference_ZE)))))),
                       LLI)

    default = np.zeros_like(left_motors)
    default2 = np.zeros_like(right_motors)

    # Defuzzification
    # Aggregate all three output membership functions together
    # Same aggregation and defuzzification for 2 speed outputs because same rules apply for them (with their respective MFs)
    aggregated1 = np.fmax(left_LLD, left_SLLD)
    aggregated2 = np.fmax(left_SLD, aggregated1)
    aggregated3 = np.fmax(left_SSLD, aggregated2)
    aggregated4 = np.fmax(left_SSLI, aggregated3)
    aggregated5 = np.fmax(left_SLI, aggregated4)
    aggregated6 = np.fmax(left_SMLI, aggregated5)
    aggregated7 = np.fmax(left_MLI, aggregated6)
    aggregated8 = np.fmax(left_SLLI, aggregated7)
    aggregatedLeft = np.fmax(left_LLI, aggregated8)

    aggregated12 = np.fmax(right_LRD, right_SLRD)
    aggregated22 = np.fmax(right_SRD, aggregated12)
    aggregated32 = np.fmax(right_SSRD, aggregated22)
    aggregated42 = np.fmax(right_SSRI, aggregated32)
    aggregated52 = np.fmax(right_SRI, aggregated42)
    aggregated62 = np.fmax(right_SMRI, aggregated52)
    aggregated72 = np.fmax(right_MRI, aggregated62)
    aggregated82 = np.fmax(right_SLRI, aggregated72)
    aggregatedRight = np.fmax(right_LRI, aggregated82)

    # Calculate defuzzified outputs
    speedLeft = fuzz.defuzz(left_motors, aggregatedLeft, 'mom')
    print("PWM increase for left pair of motors (defuzzified speed): " + str(float(round(speedLeft, 2))))
    speedRight = fuzz.defuzz(right_motors, aggregatedRight, 'mom')
    print("PWM increase for right pair of motors (defuzzified speed): " + str(float(round(speedRight, 2))))
    
    return speedLeft, speedRight 


if __name__=='__main__':
    
    control(45.9,52.3)
