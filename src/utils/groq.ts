import Groq from "groq-sdk";
import { LLMMessages } from "../middlewares/interfaces";

export async function groqChatCompletion(messages: LLMMessages[]) {
	let result = "";
	const response = await groq.chat.completions.create({
		messages: messages as any,
		model: "llama3-70b-8192",
	});

	if (response?.choices?.length < 0 || !response.choices[0].message?.content)
		console.log("Missing Groq response content");
	else {
		result = response.choices[0].message.content;
	}
	return result;
}