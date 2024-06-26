import React from 'react';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';
import PropTypes from 'prop-types';
import './GradientSlider.css';
import { MODEL_LABELS, getIntegDiagnosisKey } from '../../constants';

const marks = {
    // 0: '',
    1: MODEL_LABELS['integrated'][1],
    2: MODEL_LABELS['integrated'][2],
    3: MODEL_LABELS['integrated'][3],
    4: MODEL_LABELS['integrated'][4]
    // 5: 
    // 8: '',
};

const GradientSlider = ({ value }) => {
    return (
        <div className="slider-container">
            <Slider
                min={1}
                max={4}
                marks={marks}
                defaultValue={2}
                value={getIntegDiagnosisKey('integrated', value)}
                disabled
                trackStyle={{ backgroundColor: 'transparent' }}
                handleStyle={{ backgroundColor: 'white', borderColor: 'gray' }}
                railStyle={{ backgroundImage: 'linear-gradient(to right, green, red)' }}
            />
        </div>
    );
};

GradientSlider.propTypes = {
    value: PropTypes.string.isRequired
};

export default GradientSlider;
