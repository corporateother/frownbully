import { useState, useEffect, useRef, useCallback } from 'react';
import { Video, VideoOff, Settings as SettingsIcon, Timer, PieChart } from 'lucide-react';
// Assuming sonner is available or will be treated as external. We'll stick to console.log/error to prevent further import errors.
// import { toast } from 'sonner@2.0.3';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts'; // Using recharts for chart

// --- UTILITY COMPONENTS (Local replacements for external/non-local imports) ---

// Custom icon matching the Frown Bully design
const FrownBullyLogoIcon: React.FC<{ className?: string }> = ({ className = "w-5 h-5" }) => (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        {/* Main Head Circle */}
        <circle cx="16" cy="16" r="14" fill="#FFC0CB" stroke="#FFFFFF" strokeWidth="3" />
        {/* Smiling Mouth (Upward Curve - representing "Stay mindful") */}
        <path d="M10 18 C 12 22, 20 22, 22 18" stroke="#7E22CE" strokeWidth="2" fill="none" />
        {/* Left Eye (Dot for simplicity) */}
        <circle cx="12" cy="12" r="1.5" fill="#7E22CE" />
        {/* Right Eye (Dot for simplicity) */}
        <circle cx="20" cy="12" r="1.5" fill="#7E22CE" />
        {/* Forehead/Frown Lines (Subtle curves for awareness) */}
        <path d="M12 8 L 14 9 L 18 9 L 20 8" stroke="#7E22CE" strokeWidth="1" fill="none" strokeDasharray="1 1" />
    </svg>
);


// Placeholder for `Card` (using Tailwind classes directly)
const Card: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = "" }) => (
    <div className={`rounded-xl p-5 ${className}`}>
        {children}
    </div>
);

// Placeholder for `Button` (using Tailwind classes directly)
const Button: React.FC<{ children: React.ReactNode; onClick: () => void; disabled?: boolean; className?: string; variant?: "outline" | "default" }> = ({ children, onClick, disabled = false, className = "", variant = "default" }) => {
    const baseClasses = "py-2 px-4 rounded-lg font-semibold transition duration-150 ease-in-out shadow-md";
    const defaultClasses = "bg-blue-500 hover:bg-blue-600 text-white";
    const outlineClasses = "border border-purple-300 hover:bg-purple-50 text-purple-700 bg-white";

    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`${baseClasses} ${variant === "outline" ? outlineClasses : defaultClasses} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
        >
            {children}
        </button>
    );
};

// Placeholder for `Badge`
const Badge: React.FC<{ children: React.ReactNode; className?: string; variant?: "secondary" | "default" }> = ({ children, className = "", variant = "default" }) => {
    const baseClasses = "inline-flex items-center rounded-full px-3 py-0.5 text-xs font-medium";
    const defaultClasses = "bg-green-100 text-green-700";
    const secondaryClasses = "bg-gray-100 text-gray-600";
    return (
        <span className={`${baseClasses} ${variant === "secondary" ? secondaryClasses : defaultClasses} ${className}`}>
            {children}
        </span>
    );
};

// Placeholder for `Switch`
const Switch: React.FC<{ checked: boolean; onCheckedChange: (checked: boolean) => void; id: string }> = ({ checked, onCheckedChange, id }) => (
    <button
        role="switch"
        aria-checked={checked}
        onClick={() => onCheckedChange(!checked)}
        className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out ${checked ? 'bg-indigo-600' : 'bg-gray-200'}`}
    >
        <span
            className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${checked ? 'translate-x-5' : 'translate-x-0'}`}
        />
    </button>
);

// Placeholder for `Label`
const Label: React.FC<{ children: React.ReactNode; htmlFor: string; className?: string }> = ({ children, htmlFor, className = "" }) => (
    <label htmlFor={htmlFor} className={`text-sm ${className}`}>
        {children}
    </label>
);

// Placeholder for `Toaster` (empty for simplicity)
const Toaster = () => null;


// Placeholder for `StatsCard`
interface StatsCardProps {
    label: string;
    value: number;
    color: "blue" | "indigo" | "purple" | "pink";
    delay: number; // Unused, kept for compatibility
}
const StatsCard: React.FC<StatsCardProps> = ({ label, value, color }) => {
    const colorClasses = {
        blue: "bg-blue-50 border-blue-200 text-blue-700",
        indigo: "bg-indigo-50 border-indigo-200 text-indigo-700",
        purple: "bg-purple-50 border-purple-200 text-purple-700",
        pink: "bg-pink-50 border-pink-200 text-pink-700",
    }[color];
    return (
        <div className={`p-3 rounded-lg border shadow-sm ${colorClasses}`}>
            <p className="text-xs font-medium opacity-80">{label}</p>
            <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
    );
};

// Interface for Historical Chart Data
interface DailyData {
    date: string;
    count: number;
}

// Placeholder for `HistoricalChart`
const HistoricalChart: React.FC<{ data: DailyData[] }> = ({ data }) => {
    return (
        <Card className="bg-white/90 backdrop-blur-sm border border-purple-200 shadow-xl p-4">
            <h3 className="text-purple-900 font-semibold mb-4 flex items-center gap-2">
                <PieChart className="w-4 h-4 text-purple-600"/>
                Frown Count History (Mock Data)
            </h3>
            <div className="h-40 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" vertical={false} />
                        <XAxis dataKey="date" axisLine={false} tickLine={false} style={{ fontSize: '10px' }} />
                        <YAxis axisLine={false} tickLine={false} style={{ fontSize: '10px' }} domain={[0, 'auto']} />
                        <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', fontSize: '12px' }} />
                        <Line type="monotone" dataKey="count" stroke="#6366F1" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </Card>
    );
};


// --- API RESPONSE INTERFACES ---

interface Prediction {
    [key: string]: string; // e.g., "Frowning": "95.50%"
}

interface ApiStats {
    running: boolean;
    last_detection: string; // e.g., "14:30:15"
    status: string; // e.g., "Running" or "Stopped"
    latest_prediction: Prediction;
    summary: Summary;
}

// --- APP STATE INTERFACES ---

interface Summary {
    today: number;
    yesterday: number;
    thisWeek: number;
    lastWeek: number;
    history: { label: string; count: number }[];
  }

// Configuration for stats polling
const POLLING_INTERVAL_MS = 2000;
const API_BASE_URL = "/api";


export default function App() {
    const [isDetecting, setIsDetecting] = useState(false);
    const [launchOnStartup, setLaunchOnStartup] = useState(false);

    // Removed mock data
    const [appStats, setAppStats] = useState<AppStats>({
        today: 0,
        yesterday: 0,
        thisWeek: 0,
        lastWeek: 0,
        lastDetectionTime: 'N/A',
        latestPredictions: {},
      });

    const [historicalData, setHistoricalData] = useState<DailyData[]>([]);
    const detectionIntervalRef = useRef<number | null>(null);

    // --- API FETCHERS & LOGIC ---

    const fetchStats = useCallback(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stats`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data: ApiStats = await response.json();
            setIsDetecting(data.running);
            setAppStats(prev => ({
                ...prev,
                today: data.summary.today,
                yesterday: data.summary.yesterday,
                thisWeek: data.summary.thisWeek,
                lastWeek: data.summary.lastWeek,
                lastDetectionTime: data.last_detection,
                latestPredictions: data.latest_prediction,
            }));
            setHistoricalData(
                data.summary.history.map(item => ({
                    date: item.label,
                    count: item.count,
                }))
            );

            // 1. Update running status based on response
            setIsDetecting(data.running);

            // 2. Update real-time statistics based on API response
            setAppStats(prev => ({
                ...prev,
                lastDetectionTime: data.last_detection,
                latestPredictions: data.latest_prediction,
                // Historical stats (today, yesterday...) remain mock data for now.
            }));

        } catch (error) {
            console.error("Error fetching stats:", error);
            // Stop polling on error
            if (detectionIntervalRef.current) {
                clearInterval(detectionIntervalRef.current);
                detectionIntervalRef.current = null;
            }
            setIsDetecting(false);
            console.error('Connection Error: Failed to fetch detection stats from backend. Polling stopped.');
        }
    }, []);

    const startStatsPolling = useCallback(() => {
        // Clear any existing interval
        if (detectionIntervalRef.current) {
            clearInterval(detectionIntervalRef.current);
        }
        // Fetch immediately, then start the interval
        fetchStats();
        // TypeScript requires `window.setInterval` to return a number for clearInterval usage
        detectionIntervalRef.current = window.setInterval(fetchStats, POLLING_INTERVAL_MS);
        console.log("Stats polling started.");
    }, [fetchStats]);

    const stopStatsPolling = useCallback(() => {
        if (detectionIntervalRef.current) {
            clearInterval(detectionIntervalRef.current);
            detectionIntervalRef.current = null;
        }
        console.log("Stats polling stopped.");
    }, []);

    const startDetection = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/start`, { method: 'POST' });
            const data: { running: boolean } = await response.json();

            if (data.running) {
                setIsDetecting(true);
                startStatsPolling();
                console.log('Detection started');
            } else {
                console.error('Start Failed: Backend failed to start detection thread.');
            }
        } catch (error) {
            console.error('API Start Error:', error);
            console.error('API Error: Could not connect to the backend server to start detection.');
        }
    };

    const stopDetection = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stop`, { method: 'POST' });
            const data: { running: boolean } = await response.json();

            if (!data.running) {
                setIsDetecting(false);
                stopStatsPolling();
                console.log('Detection stopped');
            } else {
                console.error('Stop Failed: Backend reported detection is still running.');
            }
        } catch (error) {
            console.error('API Stop Error:', error);
            console.error('API Error: Could not connect to the backend server to stop detection.');
        }
    };

    // --- INITIALIZATION AND LIFECYCLE EFFECTS ---

    // 1. Check initial status from the API when the component mounts
    useEffect(() => {
        async function checkInitialStatus() {
            try {
                const response = await fetch(`${API_BASE_URL}/status`);
                const data: { running: boolean } = await response.json();

                if (data.running) {
                    setIsDetecting(true);
                    startStatsPolling();
                } else {
                    // Fetch stats one time to show last recorded data if detection is stopped
                    fetchStats();
                }
            } catch (error) {
                console.error("Initial status check failed:", error);
                setIsDetecting(false);
            }
        }
        checkInitialStatus();

        // Cleanup interval on unmount
        return () => {
            if (detectionIntervalRef.current) {
                clearInterval(detectionIntervalRef.current);
            }
        };
    }, [startStatsPolling, fetchStats]);


    // 2. Mock Historical Data/LocalStorage (KEEPING THIS FOR CHART FUNCTIONALITY)
    useEffect(() => {
        // Initialize with last 7 days with mock data
        const mockCounts = [8, 5, 12, 9, 11, 18, 12];
        const data: DailyData[] = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            data.push({
                date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                count: mockCounts[6 - i]
            });
        }
        setHistoricalData(data);
    }, []);

    // Placeholder for saving settings (Launch on startup)
    useEffect(() => {
        // No action for now as this requires OS integration
    }, [launchOnStartup]);


    // --- RENDERING ---

    // Placeholder for predicting analysis label/confidence
    const primaryPrediction = Object.entries(appStats.latestPredictions)[0] || null;
    const analysisTime = appStats.lastDetectionTime !== 'N/A' ? `Last analysis: ${appStats.lastDetectionTime}` : 'Awaiting first analysis...';


    return (
        // motion/AnimatePresence replaced with standard divs and Tailwind classes
        <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-pink-100 flex items-center justify-center p-4 relative overflow-hidden">
            <Toaster />

            {/* Y2K Background Elements */}
            <div className="absolute inset-0 opacity-30">
                {/* Simplified animations */}
                <div className="absolute top-10 left-10 w-32 h-32 bg-purple-200 rounded-full blur-3xl animate-pulse" />
                <div className="absolute bottom-20 right-20 w-40 h-40 bg-pink-200 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
                <div className="absolute top-1/2 left-1/3 w-24 h-24 bg-blue-200 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
            </div>

            <div className="w-full max-w-md relative z-10">
                {/* Header */}
                <div className="mb-4">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="w-10 h-10 bg-gradient-to-br from-purple-400 via-pink-400 to-indigo-400 rounded-lg flex items-center justify-center shadow-lg border-2 border-white">
                            <FrownBullyLogoIcon className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h2 className="text-xl font-bold bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 bg-clip-text text-transparent">Frown Bully</h2>
                            <p className="text-purple-800 text-xs">Stay mindful of your expressions ✨</p>
                        </div>
                    </div>
                </div>

                <div className="space-y-4">
                    {/* Status & Control Card */}
                    <Card className="bg-white/90 backdrop-blur-sm border border-purple-200 shadow-xl">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                                <h3 className="text-purple-900 font-semibold">Detection</h3>
                                {/* AnimatePresence/motion replaced with standard ternary */}
                                {isDetecting ? (
                                    <Badge className="bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 hover:from-green-100 hover:to-emerald-100 border border-green-300">
                                        <div className="w-2 h-2 bg-green-500 rounded-full mr-1.5 animate-ping-slow" />
                                        Active
                                    </Badge>
                                ) : (
                                    <Badge variant="secondary" className="bg-gray-100 text-gray-600 border border-gray-300">
                                        <div className="w-2 h-2 bg-gray-400 rounded-full mr-1.5" />
                                        Stopped
                                    </Badge>
                                )}
                            </div>
                        </div>

                        <div className="flex gap-2">
                            <Button
                                onClick={startDetection}
                                disabled={isDetecting}
                                className="flex-1 bg-gradient-to-r from-purple-500 via-indigo-500 to-blue-500 hover:from-purple-600 hover:via-indigo-600 hover:to-blue-600 text-white shadow-md"
                            >
                                <Video className="w-4 h-4 mr-2" />
                                Start
                            </Button>
                            <Button
                                onClick={stopDetection}
                                disabled={!isDetecting}
                                variant="outline"
                                className="flex-1 flex items-center justify-center" // Center content for outline button
                            >
                                <VideoOff className="w-4 h-4 mr-2" />
                                Stop
                            </Button>
                        </div>

                        {/* Real-time Analysis Display */}
                        <div className="mt-4 pt-4 border-t border-purple-100 space-y-2">
                            <div className="flex items-center gap-2 text-xs text-purple-700">
                                <Timer className="w-3 h-3"/>
                                <span className="font-semibold">{analysisTime}</span>
                            </div>
                            {primaryPrediction && (
                                <div className="text-sm font-medium text-purple-900">
                                    Current Mood: <span className="text-indigo-600">{primaryPrediction[0]}</span>
                                    &nbsp;({primaryPrediction[1]})
                                </div>
                            )}
                            {!primaryPrediction && isDetecting && (
                                <div className="text-sm text-gray-500 italic">Waiting for first prediction...</div>
                            )}
                        </div>
                    </Card>

                    {/* Historical Chart */}
                    <HistoricalChart data={historicalData} />

                    {/* Stats Grid */}
                    <Card className="bg-white/90 backdrop-blur-sm border border-blue-200 shadow-xl">
                        <h3 className="text-purple-900 font-semibold mb-4">Statistics ⭐</h3>

                        <div className="grid grid-cols-2 gap-3">
                            <StatsCard
                                label="Today"
                                value={appStats.today}
                                color="blue"
                                delay={0.2}
                            />
                            <StatsCard
                                label="Yesterday"
                                value={appStats.yesterday}
                                color="indigo"
                                delay={0.25}
                            />
                            <StatsCard
                                label="This Week"
                                value={appStats.thisWeek}
                                color="purple"
                                delay={0.3}
                            />
                            <StatsCard
                                label="Last Week"
                                value={appStats.lastWeek}
                                color="pink"
                                delay={0.35}
                            />
                        </div>
                    </Card>

                    {/* Settings Card */}
                    <Card className="bg-white/90 backdrop-blur-sm border border-purple-200 shadow-xl">
                        <div className="flex items-center gap-2 mb-3">
                            <SettingsIcon className="w-4 h-4 text-purple-600" />
                            <h3 className="text-purple-900 font-semibold">Settings</h3>
                        </div>

                        <div className="flex items-center justify-between">
                            <Label htmlFor="launch-startup" className="text-sm text-purple-800 cursor-pointer">
                                Launch on system startup
                            </Label>
                            <Switch
                                id="launch-startup"
                                checked={launchOnStartup}
                                onCheckedChange={setLaunchOnStartup}
                            />
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    );
}