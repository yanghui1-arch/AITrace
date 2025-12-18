import kubentApi from "./kubent-http";

type ChatMessage = {
  message: string
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
  chat(session_id: string | null, message: string){
    return kubentApi.post<Response<ChatMessage>>(
      "/chat/optimize",
      { session_id, message }
    );
  }
}
