import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ArrowUp } from "lucide-react";
import { type KeyboardEvent } from "react";

type ChatInputProps = {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  placeholder?: string;
  disabled?: boolean;
};

type ChatInputToolBarProps = {
  onSend: () => void;
  disabled?: boolean;
}

export function ChatInputToolBar({ onSend, disabled }: ChatInputToolBarProps) {
  return (
    <div className="flex items-center justify-end gap-2 dark:bg-input/30 bg-transparent px-2 py-2">
      <Button
        type="button"
        onClick={onSend}
        disabled={disabled}
        size="icon"
        className="h-9 w-9 rounded-full"
        aria-label="Send message"
      >
        <ArrowUp className="h-4 w-4" />
      </Button>
    </div>
  );
}

export function ChatInput({
  value,
  onChange,
  onSend,
  placeholder,
  disabled,
}: ChatInputProps) {
  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSend();
    }
  };

  const minRows = 1;
  const maxRows = 5;
  const rows = Math.min(
    maxRows,
    Math.max(
      minRows,
      value.split(/\r\n|\r|\n/).length,
      Math.ceil(value.length / 80)
    )
  );

  return (
    <div className="w-full overflow-hidden rounded-md border bg-background">
      <Textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder || "Ask Kubent about your project"}
        disabled={disabled}
        rows={rows}
        className="border-0 bg-transparent pt-3 pb-2 shadow-none focus-visible:ring-0 resize-none max-h-[20vh] min-h-[2.75rem] overflow-y-auto"
      />
      <ChatInputToolBar onSend={onSend} disabled={disabled}/>
    </div>
  );
}
