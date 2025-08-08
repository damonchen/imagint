import React, { useState } from 'react';
import { ChevronDown, RotateCcw } from 'lucide-react';

const AdvancedSettings = () => {
    const [isExpanded, setIsExpanded] = useState(true);
    const [randomizeSeed, setRandomizeSeed] = useState(true);
    const [seed, setSeed] = useState(5.6);
    const [width, setWidth] = useState(1024);
    const [height, setHeight] = useState(1024);
    const [guidanceScale, setGuidanceScale] = useState(4.5);
    const [inferenceSteps, setInferenceSteps] = useState(28);

    const SliderComponent = ({ label, value, onChange, min = 0, max = 100, step = 1, showRefresh = false }) => (
        <div className="space-y-2">
            <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">{label}</label>
                <div className="flex items-center gap-2">
                    <input
                        type="number"
                        value={value}
                        onChange={(e) => onChange(Number(e.target.value))}
                        className="w-16 px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-orange-500"
                    />
                    {showRefresh && (
                        <button className="p-1 hover:bg-gray-100 rounded">
                            <RotateCcw size={14} className="text-gray-500" />
                        </button>
                    )}
                </div>
            </div>
            <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500">{min}</span>
                <div className="flex-1 relative">
                    <input
                        type="range"
                        min={min}
                        max={max}
                        step={step}
                        value={value}
                        onChange={(e) => onChange(Number(e.target.value))}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                        style={{
                            background: `linear-gradient(to right, #fb923c 0%, #fb923c ${((value - min) / (max - min)) * 100}%, #e5e7eb ${((value - min) / (max - min)) * 100}%, #e5e7eb 100%)`
                        }}
                    />
                </div>
                <span className="text-xs text-gray-500">{max}</span>
            </div>
        </div>
    );

    return (
        <div className="w-full max-w-2xl mx-auto bg-white border border-gray-200 rounded-lg">
            {/* Header */}
            <div
                className="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-50"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <h3 className="text-sm font-medium text-gray-700">Advanced Settings</h3>
                <ChevronDown
                    size={16}
                    className={`text-gray-500 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                />
            </div>

            {/* Content */}
            {isExpanded && (
                <div className="p-4 pt-0 space-y-6">
                    {/* Seed Section */}
                    <div className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-700">Seed</label>
                            <div className="flex items-center gap-2">
                                <div className="flex items-center gap-2 text-xs text-orange-500">
                                    🎲 {seed}s
                                </div>
                                <button className="p-1 hover:bg-gray-100 rounded">
                                    <RotateCcw size={14} className="text-gray-500" />
                                </button>
                            </div>
                        </div>

                        <div className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                id="randomize-seed"
                                checked={randomizeSeed}
                                onChange={(e) => setRandomizeSeed(e.target.checked)}
                                className="w-4 h-4 text-orange-500 border-gray-300 rounded focus:ring-orange-500"
                            />
                            <label htmlFor="randomize-seed" className="text-sm text-gray-700">
                                Randomize seed
                            </label>
                        </div>
                    </div>

                    {/* Width and Height */}
                    <div className="grid grid-cols-2 gap-6">
                        <SliderComponent
                            label="Width"
                            value={width}
                            onChange={setWidth}
                            min={256}
                            max={2048}
                            step={64}
                            showRefresh={true}
                        />
                        <SliderComponent
                            label="Height"
                            value={height}
                            onChange={setHeight}
                            min={256}
                            max={2048}
                            step={64}
                            showRefresh={true}
                        />
                    </div>

                    {/* Guidance Scale and Inference Steps */}
                    <div className="grid grid-cols-2 gap-6">
                        <SliderComponent
                            label="Guidance Scale"
                            value={guidanceScale}
                            onChange={setGuidanceScale}
                            min={1}
                            max={15}
                            step={0.1}
                            showRefresh={true}
                        />
                        <SliderComponent
                            label="Number of inference steps"
                            value={inferenceSteps}
                            onChange={setInferenceSteps}
                            min={1}
                            max={50}
                            step={1}
                            showRefresh={true}
                        />
                    </div>
                </div>
            )}

            {/* <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 18px;
          width: 18px;
          border-radius: 50%;
          background: #fb923c;
          cursor: pointer;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }
        
        .slider::-moz-range-thumb {
          height: 18px;
          width: 18px;
          border-radius: 50%;
          background: #fb923c;
          cursor: pointer;
          border: none;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }
      `}</style> */}
        </div>
    );
};

export default AdvancedSettings;