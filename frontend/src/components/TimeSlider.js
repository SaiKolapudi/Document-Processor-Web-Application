import React from "react";

const TimeSlider = ({ dates, selectedDate, onDateChange }) => {
  return (
    <div>
      <input
        type="range"
        min={0}
        max={dates.length - 1}
        value={dates.indexOf(selectedDate)}
        onChange={(e) => onDateChange(dates[e.target.value])}
      />
      <span>{selectedDate}</span>
    </div>
  );
};

export default TimeSlider;