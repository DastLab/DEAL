const { OpenAI } = require('openai');
const openai = new OpenAI({ apiKey: process.env.REACT_APP_API_KEY_CHATGPT, dangerouslyAllowBrowser: true});

const chatGPTHandleUserInput = async (input) => {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: input }],
      max_tokens: 2048,
    });

    const assistantResponse = response.choices[0].message.content;
    return assistantResponse;

  } catch (error) {
    alert('Error: ' + error);
  }
};

module.exports = { chatGPTHandleUserInput };