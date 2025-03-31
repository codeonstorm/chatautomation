"use client"
import { useState, useEffect } from "react";
import Head from "next/head";

interface Progress {
  [key: string]: number;
}

export default function Home() {
  const [uploading, setUploading] = useState<boolean>(false);
  const [progress, setProgress] = useState<Progress>({});

  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/resumablejs/resumable.js";
    script.async = true;
    document.body.appendChild(script);
    script.onload = () => {
      const r = new Resumable({
        target: "http://127.0.0.1:8000/api/v1/1/filemanager/uploads",
        chunkSize: 1 * 1024 * 1024,
        simultaneousUploads: 3,
        testChunks: true,
      });

      r.assignBrowse(document.getElementById("fileInput") as HTMLElement);

      r.on("fileAdded", (file: any) => {
        setUploading(true);
        setProgress((prev) => ({ ...prev, [file.uniqueIdentifier]: 0 }));
        r.upload();
      });

      r.on("fileProgress", (file: any) => {
        const progressPercentage = Math.floor(file.progress() * 100);
        setProgress((prev) => ({
          ...prev,
          [file.uniqueIdentifier]: progressPercentage,
        }));
      });

      r.on("fileSuccess", (file: any) => {
        setProgress((prev) => ({ ...prev, [file.uniqueIdentifier]: 100 }));
        setUploading(false);
      });

      r.on("fileError", (file: any, message: string) => {
        alert(`Error uploading ${file.fileName}: ${message}`);
        setUploading(false);
      });
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <Head>
        <title>Next.js File Upload</title>
      </Head>
      <div className="bg-white p-6 rounded-2xl shadow-xl w-full max-w-lg">
        <h1 className="text-xl font-bold mb-4">Upload Files</h1>
        <input id="fileInput" type="file" multiple className="mb-4" />
        {uploading && (
          <div className="mt-4">
            {Object.entries(progress).map(([key, value]) => (
              <div key={key} className="mb-2">
                <span className="text-gray-600">File {key}: </span>
                <span className="font-semibold">{value}%</span>
                <div className="w-full bg-gray-300 rounded-full h-2.5">
                  <div
                    className="bg-blue-600 h-2.5 rounded-full"
                    style={{ width: `${value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
