import React, { useState } from "react";
import axios from "axios";

const DocumentUploadScreen = () => {
  const [question, setQuestion] = useState("");
  const [documents, setDocuments] = useState([]);
  const [autoApprove, setAutoApprove] = useState(false);

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleDocumentsChange = (e) => {
    setDocuments(Array.from(e.target.files));
  };

  const handleAutoApproveChange = (e) => {
    setAutoApprove(e.target.checked);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("question", question);
    documents.forEach((document) => {
      formData.append("documents", document);
    });
    formData.append("autoApprove", autoApprove);

    try {
      await axios.post("/submit_question_and_documents", formData);
      // Handle success response
    } catch (error) {
      console.error("Error submitting documents:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="question">Question:</label>
        <input
          type="text"
          id="question"
          value={question}
          onChange={handleQuestionChange}
        />
      </div>
      <div>
        <label htmlFor="documents">Documents:</label>
        <input
          type="file"
          id="documents"
          multiple
          onChange={handleDocumentsChange}
        />
      </div>
      <div>
        <label htmlFor="autoApprove">Auto Approve:</label>
        <input
          type="checkbox"
          id="autoApprove"
          checked={autoApprove}
          onChange={handleAutoApproveChange}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default DocumentUploadScreen;