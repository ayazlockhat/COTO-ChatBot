import { Textarea } from "../ui/textarea";
import { cx } from 'classix';
import { Button } from "../ui/button";
import { ArrowUpIcon } from "./icons"
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

interface ChatInputProps {
    question: string;
    setQuestion: (question: string) => void;
    onSubmit: (text?: string) => void;
    isLoading: boolean;
}

const allSuggestedActions = [
    {
        title: 'What are my rights?',
        label: 'as an occupational therapist?',
        action: 'What are the professional rights and responsibilities of an occupational therapist?',
    },
    {
        title: 'How do I report concerns?',
        label: 'about a patient\'s driving?',
        action: 'As an occupational therapist, when should I report a patient\'s fitness to drive?',
    },
    {
        title: 'Establishing a private practice',
        label: 'in Ontario',
        action: 'What are the recommended practices and information for occupational therapists wishing to establish a private practice in Ontario?',
    },
    {
        title: 'Maintaining professional boundaries',
        label: 'with clients',
        action: 'How should I maintain professional boundaries with clients to prevent conflicts of interest?',
    },
    {
        title: 'Providing virtual services',
        label: 'in occupational therapy',
        action: 'What are the guidelines for providing remote (virtual) occupational therapy services?',
    },
    {
        title: 'Record keeping standards',
        label: 'for occupational therapists',
        action: 'What are the standards for record keeping in occupational therapy practice?',
    },
    {
        title: 'Understanding consent',
        label: 'in occupational therapy',
        action: 'What are the guidelines for obtaining consent from clients in occupational therapy practice?',
    },
    {
        title: 'Managing conflicts of interest',
        label: 'in practice',
        action: 'How should I identify and manage conflicts of interest in my occupational therapy practice?',
    },
];

export const ChatInput = ({ question, setQuestion, onSubmit, isLoading }: ChatInputProps) => {
    const [showSuggestions, setShowSuggestions] = useState(true);
    const [randomizedSuggestions, setRandomizedSuggestions] = useState<typeof allSuggestedActions>([]);

    useEffect(() => {
        const getRandomSuggestions = () => {
            const shuffled = [...allSuggestedActions].sort(() => 0.5 - Math.random());
            return shuffled.slice(0, 2);
        };

        setRandomizedSuggestions(getRandomSuggestions());
    }, []);

    return(
    <div className="relative w-full flex flex-col gap-4">
        {showSuggestions && (
            <div className="hidden md:grid sm:grid-cols-2 gap-2 w-full">
                {randomizedSuggestions.map((suggestedAction, index) => (
                    <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 20 }}
                    transition={{ delay: 0.05 * index }}
                    key={index}
                    className="block"
                    >
                        <Button
                            variant="ghost"
                            onClick={ () => {
                                const text = suggestedAction.action;
                                onSubmit(text);
                                setShowSuggestions(false);
                            }}
                            className="text-left border rounded-xl px-4 py-3.5 text-sm flex-1 gap-1 sm:flex-col w-full h-auto justify-start items-start"
                        >
                            <span className="font-medium">{suggestedAction.title}</span>
                            <span className="text-muted-foreground">
                            {suggestedAction.label}
                            </span>
                        </Button>
                    </motion.div>
                ))}
            </div>
        )}
        <input
        type="file"
        className="fixed -top-4 -left-4 size-0.5 opacity-0 pointer-events-none"
        multiple
        tabIndex={-1}
        />

        <Textarea
        placeholder="Send a message..."
        className={cx(
            'min-h-[24px] max-h-[calc(75dvh)] overflow-hidden resize-none rounded-xl text-base bg-muted',
        )}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();

                if (isLoading) {
                    toast.error('Please wait for the model to finish its response!');
                } else {
                    setShowSuggestions(false);
                    onSubmit();
                }
            }
        }}
        rows={3}
        autoFocus
        />

        <Button 
            className="rounded-full p-1.5 h-fit absolute bottom-2 right-2 m-0.5 border dark:border-zinc-600"
            onClick={() => onSubmit(question)}
            disabled={question.length === 0}
        >
            <ArrowUpIcon size={14} />
        </Button>
    </div>
    );
}