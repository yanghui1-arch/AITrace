import { type ChatCompletionAudio } from "openai/resources/index.mjs";
import { type Annotation } from "openai/resources/beta/threads/messages.mjs";
import { type ChatCompletionMessageToolCall } from "openai/resources/index.mjs";
import { type ChatCompletion } from "openai/resources/chat/completions/completions";
import { type CompletionUsage } from "openai/resources/index.mjs";
import { type ResponseCreateParams } from "openai/resources/responses/responses.mjs";
import type { ColumnDef } from "@tanstack/react-table";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { ArrowDown, ArrowUp, List } from "lucide-react";

/* style as the same as openai */
export interface FilteredFieldsOpenAIChatCompletionsOutput {
  model: string;
  created: string;
  content?: string;
  role?: "assistant";
  annotations?: Array<Annotation>;
  audio?: ChatCompletionAudio;
  tool_calls?: Array<ChatCompletionMessageToolCall>;
  choices: Array<ChatCompletion.Choice>;
  service_tier?: "auto" | "default" | "flex" | "scale" | "priority";
  system_fingerprint?: string;
  usage?: CompletionUsage;
}

export interface InputData {
  funcInput: object;
  llmInput?: ResponseCreateParams;
}

export interface OutputData {
  funcOutput?: object | string;
  llmOutput?: FilteredFieldsOpenAIChatCompletionsOutput;
}

export type Step = {
  id: string;
  name: string;
  type: "customized" | "llm_response" | "retrieve" | "tool";
  input: Array<InputData>;
  output: Array<OutputData>;
  tags: Array<string>;
  errorInfo?: string;
  model: string;
  usage?: CompletionUsage;
  startTime: string;
  endTime: string;
};

export const stepColumns: ColumnDef<Step>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
  },
  {
    accessorKey: "id",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          className="w-full justify-center"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          <span className="inline-flex items-center justify-center gap-1">
            <span className="w-4 inline-flex justify-end">
              <List className="h-4 w-4" />
            </span>
            <span className="font-semibold">ID</span>
            <span className="w-4 inline-flex justify-start">
              {column.getIsSorted() === "asc" ? (
                <ArrowDown className="h-4 w-4" />
              ) : (
                <ArrowUp className="h-4 w-4" />
              )}
            </span>
          </span>
        </Button>
      );
    },
  },
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          className="w-full justify-center"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          <span className="inline-flex items-center justify-center gap-1">
            <span className="w-4 inline-flex justify-end">
              <List className="h-4 w-4" />
            </span>
            <span className="font-semibold">Name</span>
            <span className="w-4 inline-flex justify-start">
              {column.getIsSorted() === "asc" ? (
                <ArrowDown className="h-4 w-4" />
              ) : (
                <ArrowUp className="h-4 w-4" />
              )}
            </span>
          </span>
        </Button>
      );
    },
  },
  {
    accessorKey: "startTime",
    header: () => (
      <div className="w-full flex justify-center">
        <span className="font-semibold">Start Time</span>
      </div>
    ),
    cell: ({ row }) => {
      const startTime = row.original.startTime;
      return (
        <div className="text-center font-medium">{startTime}</div>
      );
    },
  },
  {
    accessorKey: "endTime",
    header: () => (
      <div className="w-full flex justify-center">
        <span className="font-semibold">End Time</span>
      </div>
    ),
    cell: ({ row }) => {
      const endTime = row.original.endTime;
      return (
        <div className="text-center font-medium">{endTime}</div>
      );
    },
  },
];
