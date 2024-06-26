// src/constants.js
// NOTE same as utils.py in backend...
export const MODEL_LABELS = {
    rf: {
        0: '< 50% diameter narrowing in major vessel. (angiographic disease ABSENT)',
        1: '> 50% diameter narrowing in major vessel. (angiographic disease PRESENT)'
    },
    ecg: {
        0: 'The patient is more likely to be healthy.',
        1: 'The patient is more likely to have Myocardial Infarction (MI).'
    },
    echo: {
        0: 'Not Myocardial Infarction.',
        1: 'Myocardial Infarction.'
    },
    integrated: {
        1: 'healthy',
        2: 'low risk/ damage',
        3: 'unqualified/ congenital damage',
        4: 'high risk'
    }
};


export function getIntegDiagnosisKey(model, string) {
    const modelLabels = MODEL_LABELS[model];
    for (const key in modelLabels) {
        if (modelLabels[key] === string) {
            return key;
        }
    }
    return null;
}