import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Update with your backend API URL

export const submitQuestionAndDocuments = async (question, documents, autoApprove) => {
  const formData = new FormData();
  formData.append('question', question);
  documents.forEach((document) => {
    formData.append('documents', document);
  });
  formData.append('autoApprove', autoApprove);

  try {
    const response = await axios.post(`${API_URL}/submit_question_and_documents`, formData);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export const getQuestionAndFacts = async () => {
  try {
    const response = await axios.get(`${API_URL}/get_question_and_facts`);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};