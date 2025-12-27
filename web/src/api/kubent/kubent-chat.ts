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
  title: string | undefined;
  last_update_timestamp: string;
}

type KubentChat = {
  role: "user" | "assistant";
  content: string;
  start_timestamp: string;
}

export const kubentChatApi = {
  /* Get chat session */
  session(){
    return kubentApi.get<Response<KubentChatSession[]>>(
      "/query/session",
    );
  },
  createSession() {
    return kubentApi.post<Response<KubentChatSession>>(
      "/chat/create_chat_session"
    );
  },
  queryChats(session_id: string) {
    return kubentApi.get<Response<KubentChat[]>>(
      `/query/chats?session_id=${session_id}`,
    );
  },
  chat(session_id: string | undefined, message: string, project_id: number){
    return kubentApi.post<Response<ChatMessage>>(
      "/chat/optimize",
      { session_id, message, project_id }
    );
  },
  title(session_id: string, message: string) {
    return kubentApi.post<Response<string>>(
      "/chat/title",
      { session_id, message }
    );
  }
}
