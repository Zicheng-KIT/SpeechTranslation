trimmed_europarl: 2506 samples

trimmed_europarl_0: 
- not-fine-tuned model
- prompt: "Listen to the speech and translate it into English."
- BLEU score: 13.76
- Number of samples: 2506

trimmed_europarl_1: 
- prompt: "Listen to the speech and translate it into English."
- BLEU score: 19.58
- Number of samples: 2506

trimmed_europarl_2:
- prompt: "Listen to the German speech of the european parliament and translate it into English."
- BLEU score: 20.55
- Number of samples: 2506

trimmed_europarl_3:
- prompt: “You are an expert translator for German to English. Listen carefully to the German speech from the European Parliament. Maintain the formal tone and ensure political, cultural, and linguistic nuances are preserved. Translate the speech into clear and professional English, suitable for publication.”
- BLEU score: 20.97
- Number of samples: 2325

trimmed_europarl_4:
- prompt: 
"""System / Role:
You are a professional translator working in the European Parliament. Your primary task is to accurately transcribe German speeches from parliamentary sessions and translate them into precise, fluent English.

	Instructions:
	1.	Context: You have access to German-language speeches from the European Parliament.
	2.	Transcription: You must treat the source text as verbatim German parliamentary speech.
	3.	Translation: Provide an English translation that is faithful to the speaker’s intent, tone, and style. Your translation should be polished and use natural, idiomatic English.
	4.	Clarity & Formality: Because this is an official context, maintain a professional and formal register. Avoid adding or removing content.
	6.	No Other Languages: Only focus on German to English translations. Do not process or translate text in other languages."""

- BLEU score: 11.37
- Number of samples: 1544

Lines 10/11 for reference that it repeats the prompt
Line 22 that it doesn't translate but just outputs English
Line 39 for Chinese
Line 130 Does not recognize any speech