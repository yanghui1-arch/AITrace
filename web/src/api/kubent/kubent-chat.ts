import kubentApi from "./kubent-http";

type ChatMessage = {
  role: "assistant" | "user";
  content: string;
};

type Response<T> = {
  code: number;
  message: string;
  data: T
}

type Session = {
  id: string;
  chat_history: ChatMessage[];
}

export const kubentChatApi = {
  /* Get chat session */
  session(session_id: string){
    return kubentApi.post<Response<Session>>(
      "/session",
      session_id,
    );
  },
  chat(history_chat_message: ChatMessage[]){
    return kubentApi.post<Response<ChatMessage>>(
      "/chat",
      history_chat_message,
    );
  }
}
