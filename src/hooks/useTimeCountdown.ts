"use client";

import { useState, useCallback } from 'react';

const useTimeCountdown = () => {
    const [currentCountdown, setCurrentCountdown] = useState<number | null>(null);

    const startCountdown = useCallback((secondsPerItem: number, numberOfItems: number, onComplete: () => void) => {
        const totalSeconds = secondsPerItem * numberOfItems;

        setCurrentCountdown(totalSeconds);

        const interval = setInterval(() => {
            setCurrentCountdown(prevCountdown => {
                if (prevCountdown === null || prevCountdown <= 1) {
                    clearInterval(interval);
                    onComplete();
                    return null;
                }

                return prevCountdown - 1;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return { currentCountdown, startCountdown };
};

export default useTimeCountdown;