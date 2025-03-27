import { ThemeToggle } from "./theme-toggle";
// @ts-ignore
import { Github } from "lucide-react";
import { Button } from "@/components/ui/button"; 
import { FC } from "react";

interface HeaderProps {
  selectedModel: string;
  onModelChange: (model: string) => void;
}

export const Header: FC<HeaderProps> = ({ selectedModel, onModelChange }) => {
  return (
    <header className="flex items-center justify-between px-2 sm:px-4 py-2 bg-background text-black dark:text-white w-full">
      <div className="flex items-center space-x-1 sm:space-x-2">
        <ThemeToggle />
      </div>

      <div className="flex flex-col items-center">
        <span className="font-semibold text-lg">ChatOTP</span>
        <select
          value={selectedModel}
          onChange={(e) => onModelChange(e.target.value)}
          className="bg-background text-xs text-gray-500 dark:text-gray-400 border rounded px-2 mt-1"
        >
          <option value="gpt-4o-mini">GPT-4o mini</option>
          <option value="gemini-2.5-pro-exp-03-25">Gemini 2.5 Pro exp-03-25</option>
        </select>
      </div>

      <div className="w-[40px] sm:w-[48px]">
        <Button
          variant="outline"
          className="bg-background border text-gray-600 hover:white dark:text-gray-200 h-10"
          asChild
        >
          <a
            href="https://github.com/ayazzlockhat/COTO-ChatBot"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center w-full h-full"
          >
            <Github className="h-[1.2rem] w-[1.2rem]" />
          </a>
        </Button>
      </div>
    </header>
  );
};
