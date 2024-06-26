import unittest



# 0 is healthy
# 1 is sick
MODEL_LABELS = {
    'rf': {
        0: '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)',
        1: '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
    },
    'ecg': {
        0: 'The patient is more likely to be healthy.',
        1: 'The patient is more likely to have Myocardial Infarction (MI).'
    },
    'echo': {
        0: 'Not Myocardial Infarction.',
        1: 'Myocardial Infarction.'
    },
    'integrated': {
        1: 'healthy',
        2: 'low risk/ damage',
        3: 'unqualified/ congenital damage',
        4: 'high risk'
    }
}

#  This function is the truth table
def integ_diagnose(rf_string, ecg_string, echo_string):
    rf_diagnosis = get_integ_diagnosis_key('rf', rf_string)
    ecg_diagnosis = get_integ_diagnosis_key('ecg', ecg_string)
    echo_diagnosis = get_integ_diagnosis_key('echo', echo_string)


    # Case 1: using only one model
    if (rf_diagnosis is None and ecg_diagnosis is None):
        return 1 if echo_diagnosis==0 else 4
    if (rf_diagnosis is None and echo_diagnosis is None):
        return 1 if ecg_diagnosis==0 else 4
    if (ecg_diagnosis is None and echo_diagnosis is None):
        return 1 if rf_diagnosis==0 else 4
    

    # Case 2.a: using two models that produce an intermediate label
    if echo_diagnosis is None:
        return 4 if ecg_diagnosis == 1 else 1
    
    # Case 2.b: using two models that DON’T produce an intermediate label
    if rf_diagnosis is None:
        rf_diagnosis = ecg_diagnosis
    if ecg_diagnosis is None:
        ecg_diagnosis = rf_diagnosis




    intermediate = (ecg_diagnosis == 1)

    if intermediate == 0 and echo_diagnosis == 0:
        integrated = 1
    elif intermediate == 1 and echo_diagnosis == 0:
        integrated = 2
    elif intermediate == 0 and echo_diagnosis == 1:
        integrated = 3
    elif intermediate == 1 and echo_diagnosis == 1:
        integrated = 4

    return integrated

# integ_diagnose (Truth table function) helper
def get_integ_diagnosis_key(model, string):
    for key, value in MODEL_LABELS[model].items():
        if value == string:
            return key
    return None












class TestHeartAttackPrediction(unittest.TestCase):

    def test_case_1(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)'
        ecg_string = 'The patient is more likely to be healthy.'
        echo_string = 'Not Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 1)

    def test_case_2(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)'
        ecg_string = 'The patient is more likely to have Myocardial Infarction (MI).'
        echo_string = 'Not Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 2)

    def test_case_3(self):
        rf_string = '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
        ecg_string = 'The patient is more likely to be healthy.'
        echo_string = 'Not Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 1)

    def test_case_4(self):
        rf_string = '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
        ecg_string = 'The patient is more likely to have Myocardial Infarction (MI).'
        echo_string = 'Not Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 2)

    def test_case_5(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)'
        ecg_string = 'The patient is more likely to be healthy.'
        echo_string = 'Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 3)

    def test_case_6(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)'
        ecg_string = 'The patient is more likely to have Myocardial Infarction (MI).'
        echo_string = 'Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 4)

    def test_case_7(self):
        rf_string = '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
        ecg_string = 'The patient is more likely to be healthy.'
        echo_string = 'Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 3)

    def test_case_8(self):
        rf_string = '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
        ecg_string = 'The patient is more likely to have Myocardial Infarction (MI).'
        echo_string = 'Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 4)

    def test_case_9(self):
        rf_string = '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
        ecg_string = ''
        echo_string = ''
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 4)

    def test_case_10(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)'
        ecg_string = ''
        echo_string = ''
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 1)

    def test_case_11(self):
        rf_string = ''
        ecg_string = ''
        echo_string = 'Myocardial Infarction.'
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 4)
    
    def test_case_12(self):
        rf_string = ''
        ecg_string = 'The patient is more likely to be healthy.'
        echo_string = ''
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 1)

    def test_case_13(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)'
        ecg_string = 'The patient is more likely to be healthy.'
        echo_string = ''
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 1)
    
    def test_case_14(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)'
        ecg_string = 'The patient is more likely to have Myocardial Infarction (MI).'
        echo_string = ''
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 4)


    def test_case_15(self):
        rf_string = '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)' # 0
        ecg_string = '' # 0
        echo_string = 'Myocardial Infarction.' # 1
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 3)
    
    def test_case_16(self):
        rf_string = '' # 1
        ecg_string = 'The patient is more likely to have Myocardial Infarction (MI).' # 1
        echo_string = 'Not Myocardial Infarction.' # 0
        result = integ_diagnose(rf_string, ecg_string, echo_string)
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
