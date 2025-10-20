import React from 'react';

const Loading = () => {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;

  const pinkArc = 0.7 * circumference;
  const whiteGap1 = 0.075 * circumference;
  const blueArc = 0.15 * circumference;
  const whiteGap2 = 0.075 * circumference;

  return (
    <div style={{
      position: 'absolute',
      top: '300px', // adjust this value as needed
      left: '50%',
      transform: 'translateX(-50%)',
    }}>
      <svg
        width="80"
        height="80"
        viewBox="0 0 100 100"
        style={{ animation: 'rotate 2s linear infinite' }}
      >
        {/* White base circle to show gaps */}
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke="white"
          strokeWidth="8"
          fill="none"
        />

        {/* Pink arc */}
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke="#FFA4F0"
          strokeWidth="8"
          fill="none"
          strokeDasharray={`${pinkArc} ${circumference - pinkArc}`}
          strokeDashoffset="0"
          strokeLinecap="round"
        />

        {/* Blue arc */}
        <circle
          cx="50"
          cy="50"
          r={radius}
          stroke="#0000FF"
          strokeWidth="8"
          fill="none"
          strokeDasharray={`${blueArc} ${circumference - blueArc}`}
          strokeDashoffset={-(pinkArc + whiteGap1)}
          strokeLinecap="round"
        />
      </svg>

      <style>{`
        @keyframes rotate {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default Loading;
