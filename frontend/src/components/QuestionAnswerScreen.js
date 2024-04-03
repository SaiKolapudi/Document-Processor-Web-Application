import React, { useState, useEffect } from "react";
import axios from "axios";
import TimeSlider from "./TimeSlider";
import FactList from "./FactList";

const QuestionAnswerScreen = () => {
  const [question, setQuestion] = useState("");
  const [factsByDay, setFactsByDay] = useState({});
  const [selectedDate, setSelectedDate] = useState(null);

  useEffect(() => {
    fetchQuestionAndFacts();
  }, []);

  const fetchQuestionAndFacts = async () => {
    try {
      const response = await axios.get("/get_question_and_facts");
      setQuestion(response.data.question);
      setFactsByDay(response.data.factsByDay);
      setSelectedDate(Object.keys(response.data.factsByDay)[0]);
    } catch (error) {
      console.error("Error fetching question and facts:", error);
    }
  };

  const handleDateChange = (date) => {
    setSelectedDate(date);
  };

  return (
    <div>
      <h2>{question}</h2>
      <TimeSlider
        dates={Object.keys(factsByDay)}
        selectedDate={selectedDate}
        onDateChange={handleDateChange}
      />
      <FactList facts={factsByDay[selectedDate] || []} />
    </div>
  );
};

export default QuestionAnswerScreen;