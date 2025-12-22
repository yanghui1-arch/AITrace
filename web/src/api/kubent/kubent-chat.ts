import kubentApi from "./kubent-http";

type ChatMessage = {
  message: string
};

type Response<T> = {
  code: number;
  message: string;
  data: T
}

type KubentChatSession = {
  id: string;
  user_id: string;
  topic: string | undefined;
  last_update_timestamp: string;
}

export const kubentChatApi = {
  /* Get chat session */
  session(){
    return kubentApi.get<Response<KubentChatSession[]>>(
      "/query/session",
    );
  },
  chat(session_id: string | null, message: string){
    return kubentApi.post<Response<ChatMessage>>(
      "/chat/optimize",
      { session_id, message }
    );
  }
}
