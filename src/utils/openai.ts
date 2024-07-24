import OpenAI from "openai";

// Add a valid API key to the .env file to the variable "OPENAI_API_KEY" to be able to use the following functions

export async function openAIRequest(prompt: string, userMessage: string): Promise<string> {
    const openai = new OpenAI();

    const response = await openai.chat.completions.create({
		messages: [{ role: "system", content: `You follow the following instructions: ${prompt}` }, { role: "user", content: userMessage }],
		model: "gpt-4o-mini",
	});

    if (!response.choices[0].message?.content) {
		console.error("OpenAIAnswer", "No response from OpenAI");
        return "No response from OpenAI";
    } else {
        return response.choices[0].message.content;
    }
}

export async function openAIJSONRequest(prompt: string, userMessage: string): Promise<{answer: string}> {
    const openai = new OpenAI();

    const JSONExample = {
        answer: "string"
    }

    const response = await openai.chat.completions.create({
		messages: [{ role: "system", content: `INSTRUCTION: You follow the following instructions: ${prompt}. 
            FORMAT: format the answer in the following JSON structure: ${JSON.stringify(JSONExample)}` }, 
            { role: "user", content: userMessage }],
		model: "gpt-4o-mini",
        response_format: { type: "json_object" }
	});

    if (response?.choices?.length || response.choices[0].message?.content) {
        const answerJSON = JSON.parse(response.choices[0].message.content as string);
        return answerJSON;
	} else {
        console.error("OpenAIAnswer", "No response from OpenAI");
        return {answer: "No response from OpenAI"};
    }
}