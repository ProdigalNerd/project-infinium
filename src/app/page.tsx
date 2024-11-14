"use client";

import useTimeCountdown from "@/hooks/useTimeCountdown";
import { FormEvent, useCallback } from "react";

export default function Home() {
  const {
    currentCountdown,
    startCountdown,
  } = useTimeCountdown();

  const handleCountdownComplete = useCallback(() => {
    alert('The fight has ended!');
  }, []);

  const onSubmit = useCallback((event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const goblins = formData.get('goblins')?.toString();

    startCountdown(5, parseInt(goblins as string), handleCountdownComplete); 
  }, [startCountdown, handleCountdownComplete]);
 
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <form
          className="flex flex-col items-center gap-4"
          onSubmit={onSubmit}
        >
            <label htmlFor="characterName" className="text-lg font-medium">
              Character Name:
            </label>
            <input
              type="text"
              id="characterName"
              name="characterName"
              className="p-2 border border-gray-300 rounded-md text-gray-800"
              placeholder="Enter your character name"
            />
            <label htmlFor="goblins" className="text-lg font-medium">
              Number of Level 1 Goblins:
            </label>
            <select
              id="goblins"
              name="goblins"
              className="p-2 border border-gray-300 rounded-md text-gray-800"
            >
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
            <button
              type="submit"
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            >
              Commence Fight
            </button>
        </form>
        <div className="flex flex-col items-center gap-4">
          <h2 className="text-2xl font-bold">Time Remaining:</h2>
          <p className="text-4xl font-semibold">{currentCountdown}</p>
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        
      </footer>
    </div>
  );
}
