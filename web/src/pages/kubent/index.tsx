import { projectApi } from "@/api/project";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useEffect, useState } from "react";
import { AssistantChatBubble, UserChatBubble } from "@/components/chat/bubble";
import { ChatInput } from "@/components/chat/input";
import { Label } from "@/components/ui/label";
import { kubentChatApi } from "@/api/kubent/kubent-chat";
import { cn } from "@/lib/utils";

type ChatMessage = {
  role: "assistant" | "user";
  content: string;
  startTimestamp: string;
};

type Session = {
  id: string;
  userId: string;
  topic: string | undefined;
  lastUpdateTimestamp: string;
};

export default function KubentPage() {
  const [projectNames, setProjectNames] = useState<string[]>([]);
  const [selectedProjectName, setSelectedProjectName] = useState<string>("");
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selectedSession, setSelectedSession] = useState<string | null>(
    null
  );
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");

  const selectProject = (projectName: string) =>
    setSelectedProjectName(projectName);

  const selectSession = async (sessionId: string) => {
    setSelectedSession(sessionId);
    try {
      const response = await kubentChatApi.queryChats(sessionId);
      if (response.data.code === 200) {
        const data = response.data.data;
        setMessages(data
          .sort((a, b) => new Date(a.start_timestamp).getTime() - new Date(b.start_timestamp).getTime())
          .map(chat => {
          return {
            role: chat.role,
            content: chat.content,
            startTimestamp: chat.start_timestamp,
          }
        }));
      } else {
        console.error(response.data.message)
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleSend = async () => {
    if (!selectedProjectName) return;
    if (!inputValue.trim()) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: inputValue.trim(),
      startTimestamp: new Date().toLocaleString("sv-SE"),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    const response = await kubentChatApi.chat(selectedSession, inputValue);
    if (response.data.code === 200) {
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.data.data.message,
        startTimestamp: new Date().toLocaleString("sv-SE"),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }
  };

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await projectApi.getAllProjects();
        if (response.data.code === 200) {
          const userProjects = response.data.data;
          const projectNames: string[] = userProjects.map((p) => p.projectName);
          setProjectNames(projectNames);
          if (projectNames.length > 0) {
            setSelectedProjectName(projectNames[0]);
          }
        }
      } catch (error) {
        console.error(error);
      }
    };
    const fetchSessions = async () => {
      try {
        const response = await kubentChatApi.session();
        if (response.data.code === 200) {
          const sessionData = response.data.data;
          setSessions(
            sessionData
            .sort((a, b) => new Date(b.last_update_timestamp).getTime() - new Date(a.last_update_timestamp).getTime())
            .map((session) => {
              return {
                id: session.id,
                userId: session.user_id,
                topic: session.topic,
                lastUpdateTimestamp: session.last_update_timestamp,
              };
            })
          );
          if (sessionData.length > 0) {
            selectSession(sessionData[0].id);
          }
        } else {
          console.error(response.data.message);
        }
      } catch (error) {
        console.error(error);
      }
    };
    fetchProjects();
    fetchSessions();
  }, []);

  return (
    <div className="flex flex-col gap-4 px-4 lg:px-6">
      <div>
        <h2 className="text-xl font-semibold">Kubent</h2>
        <p className="text-muted-foreground mt-1 text-sm">
          {selectedProjectName
            ? `Chatting about ${selectedProjectName}.`
            : "Select a project to chat with Kubent to optimize your agent system."}
        </p>
      </div>

      <div className="flex gap-2 lg:flex-row lg:items-center">
        <Label>Select one project</Label>
        <Select onValueChange={selectProject} value={selectedProjectName}>
          <SelectTrigger className="w-full lg:w-[150px]">
            <SelectValue placeholder="Select a project to optimize" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Projects</SelectLabel>
              {projectNames.map((projectName: string) => (
                <SelectItem key={projectName} value={projectName}>
                  {projectName}
                </SelectItem>
              ))}
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
      <div className="flex gap-2 w-full">
        <div className="flex h-[69vh] w-[20%] flex-col min-w-0 gap-1 p-2">
          <Label className="text-muted-foreground text-xs font-bold px-1">
            Recent
          </Label>
          <ScrollArea className="flex-1 min-h-0">
            <div className="flex w-full flex-col gap-1 pr-4">
              {sessions.map((session, i) => (
                <div
                  key={i}
                  className={cn(
                    `
                      min-w-0
                      w-[170px] px-1 py-2 rounded-md
                      cursor-pointer select-none
                      text-sm
                      hover:bg-accent hover:text-accent-foreground
                      active:bg-accent/80
                      truncate
                    `,
                    selectedSession === session.id &&
                      "bg-accent text-accent-foreground"
                  )}
                  onClick={() => selectSession(session.id)}
                >
                  {session.id}
                </div>
              ))}
            </div>
          </ScrollArea>
        </div>
        <div className="flex h-[69vh] w-full flex-col gap-4 p-2">
          <ScrollArea className="flex-1 min-h-0">
            <div className="mx-auto flex w-full max-w-4xl flex-col gap-4 py-2">
              {messages.map((message) =>
                message.role === "assistant" ? (
                  <AssistantChatBubble content={message.content} />
                ) : (
                  <UserChatBubble content={message.content} />
                )
              )}
            </div>
          </ScrollArea>

          <div className="mx-auto w-full max-w-4xl">
            <ChatInput
              value={inputValue}
              onChange={setInputValue}
              onSend={handleSend}
              placeholder={
                selectedProjectName
                  ? `Ask Kubent about ${selectedProjectName}`
                  : "Select a project to start chatting with Kubent"
              }
              disabled={!selectedProjectName}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
