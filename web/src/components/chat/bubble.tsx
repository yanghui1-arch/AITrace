import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";
import { Markdown } from "../markdown";

type ChatBubbleProps = {
  content: string;
  className?: string;
};

export function AssistantChatBubble({ content, className }: ChatBubbleProps) {
  return (
    <div className={cn("flex w-full justify-center", className)}>
      <div className="w-full max-w-5xl text-sm leading-relaxed text-justify">
        <Markdown content={content} />
      </div>
    </div>
  );
}

export function UserChatBubble({ content, className }: ChatBubbleProps) {
  return (
    <div className={cn("flex items-start justify-end gap-3", className)}>
      <Card className="max-w-[80%] bg-muted/60 p-3 text-sm leading-relaxed">
        <Markdown content={content} />
      </Card>
    </div>
  );
}
