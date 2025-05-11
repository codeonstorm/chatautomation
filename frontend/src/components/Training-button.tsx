"use client";

import type React from "react";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Play,
} from "lucide-react";
 
import { useAppDispatch, useAppSelector } from "@/redux/store/hooks";
import { useAuth } from "@/context/auth-context";
import { startDataIngestion } from "@/services/scrapedurls";
import { channel } from "diagnostics_channel";

 
interface TrainingButtonProps {
  isDataExists: number;
  chatbot_uuid: string;
  domain_uuid: string;
}

export default function TrainingButton(trainingMeta: TrainingButtonProps) {
  const params = useParams();
  const router = useRouter();

  // urls
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();

  const handleStartTraining = (chatbot_uuid: string, domain_uuid: string) => {
    if(!user?.services[0]) {
      return
    }
    setIsLoading(true);

    const startTraining = async (serviceid: number, chatbot_uuid: string, domain_uuid: string) => {
      startDataIngestion(serviceid, chatbot_uuid, domain_uuid);
    }

    startTraining(user.services[0].id, chatbot_uuid, domain_uuid);
    setTimeout(() => {
      setIsLoading(false);
      // toast({
      //   title: "Training started",
      //   description: "Your chatbot is now being trained with the provided data.",
      // })
    }, 2000);
  };

  return (
    <div className="mt-8">
      <Separator className="my-6" />
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold mb-2">Start Training</h2>
          <p className="text-muted-foreground">
            Train your chatbot with the data you've provided. This process may
            take some time depending on the amount of data.
          </p>
        </div>
        <Button
          size="lg"
          onClick={() => {handleStartTraining(trainingMeta.chatbot_uuid, trainingMeta.domain_uuid)}}
          disabled={isLoading || trainingMeta.isDataExists === 0}
          className="gap-2"
        >
          {isLoading ? (
            <>Processing...</>
          ) : (
            <>
              <Play className="h-4 w-4" /> Start Training
            </>
          )}
        </Button>
      </div>
    </div>
  );
}
