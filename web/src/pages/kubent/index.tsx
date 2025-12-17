import { projectApi } from "@/api/project";
import { Card } from "@/components/ui/card";
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
import {
  AssistantChatBubble,
  UserChatBubble,
} from "@/components/chat/bubble";
import { ChatInput } from "@/components/chat/input";

type ChatMessage = {
  id: string;
  role: "assistant" | "user";
  content: string;
};

export default function KubentPage() {
  const [projectNames, setProjectNames] = useState<string[]>([]);
  const [selectedProjectName, setSelectedProjectName] = useState<string>();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "user-1",
      role: "user",
      content: "Great. I want to reduce latency for my order-processing agent.",
    },
    {
      id: "assistant-1",
      role: "assistant",
      content:
        "Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.Hi! Select a project and tell me what you need optimized. I will review your agent setup and suggest changes.",
    },
  ]);
  const [inputValue, setInputValue] = useState("");

  const selectProject = (projectName: string) =>
    setSelectedProjectName(projectName);

  const handleSend = () => {
    if (!selectedProjectName) return;
    if (!inputValue.trim()) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: inputValue.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
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
    fetchProjects();
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

      <div className="flex flex-col gap-2 lg:flex-row lg:items-center">
        <Select onValueChange={selectProject} value={selectedProjectName}>
          <SelectTrigger className="w-full lg:w-[280px]">
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

      <Card className="flex h-[69vh] flex-col gap-4 p-4">
        <ScrollArea className="flex-1 h-12">
          <div className="mx-auto flex w-full max-w-3xl flex-col gap-4 py-2">
            {messages.map((message) =>
              message.role === "assistant" ? (
                <AssistantChatBubble
                  key={message.id}
                  content={message.content}
                />
              ) : (
                <UserChatBubble key={message.id} content={message.content} />
              )
            )}
          </div>
        </ScrollArea>

        <div className="mx-auto w-full max-w-3xl">
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
      </Card>
    </div>
  );
}
