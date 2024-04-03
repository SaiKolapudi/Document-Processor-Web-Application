import React from "react";

const FactList = ({ facts }) => {
  return (
    <ul>
      {facts.map((fact, index) => (
        <li key={index}>{fact}</li>
      ))}
    </ul>
  );
};

export default FactList;