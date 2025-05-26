import React, { useState, useEffect } from 'react'
import Head from 'next/head'
import { ConnectButton } from '@rainbow-me/rainbowkit'
import { useAccount } from 'wagmi'
import { motion } from 'framer-motion'
import { 
  Shield, 
  Zap, 
  Brain, 
  Target, 
  Activity, 
  TrendingUp,
  AlertTriangle,
  Users,
  Clock,
  Award
} from 'lucide-react'
import ThreatIntelligence from '../components/ThreatIntelligence'
import AttackSimulation from '../components/AttackSimulation'
import WarGames from '../components/WarGames'
import RealTimeAnalytics from '../components/RealTimeAnalytics'
import SmartContractAnalyzer from '../components/SmartContractAnalyzer'

export default function Dashboard() {
  const { address, isConnected } = useAccount()
  const [activeTab, setActiveTab] = useState('dashboard')
  const [realTimeData, setRealTimeData] = useState({
    activeThreats: 0,
    simulationsRunning: 0,
    contractsAnalyzed: 0,
    defenseEffectiveness: 0
  })

  useEffect(() => {
    // Simulate real-time data updates
    const interval = setInterval(() => {
      setRealTimeData({
        activeThreats: Math.floor(Math.random() * 50) + 10,
        simulationsRunning: Math.floor(Math.random() * 20) + 5,
        contractsAnalyzed: Math.floor(Math.random() * 100) + 50,
        defenseEffectiveness: Math.random() * 0.3 + 0.7
      })
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'threats', label: 'Threat Intel', icon: AlertTriangle },
    { id: 'simulation', label: 'Attack Sim', icon: Target },
    { id: 'analyzer', label: 'Contract Analyzer', icon: Brain },
    { id: 'wargames', label: 'War Games', icon: Users },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp }
  ]

  const StatCard = ({ title, value, icon: Icon, trend, color = "blue" }: any) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6 hover:border-${color}-500/50 transition-all duration-300`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm font-medium">{title}</p>
          <p className={`text-2xl font-bold text-${color}-400 mt-1`}>{value}</p>
          {trend && (
            <p className={`text-sm mt-2 ${trend > 0 ? 'text-green-400' : 'text-red-400'}`}>
              {trend > 0 ? '↗' : '↘'} {Math.abs(trend)}% from last hour
            </p>
          )}
        </div>
        <Icon className={`w-8 h-8 text-${color}-400`} />
      </div>
    </motion.div>
  )

  const renderTabContent = () => {
    switch (activeTab) {
      case 'threats':
        return <ThreatIntelligence />
      case 'simulation':
        return <AttackSimulation />
      case 'analyzer':
        return <SmartContractAnalyzer />
      case 'wargames':
        return <WarGames />
      case 'analytics':
        return <RealTimeAnalytics />
      default:
        return (
          <div className="space-y-8">
            {/* Hero Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-12"
            >
              <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent mb-4">
                Quantum-AI Cyber God
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                The Ultimate Web3 Defense System - Protecting the future of decentralized technology
              </p>
            </motion.div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard
                title="Active Threats"
                value={realTimeData.activeThreats}
                icon={AlertTriangle}
                trend={-12}
                color="red"
              />
              <StatCard
                title="Simulations Running"
                value={realTimeData.simulationsRunning}
                icon={Target}
                trend={8}
                color="yellow"
              />
              <StatCard
                title="Contracts Analyzed"
                value={realTimeData.contractsAnalyzed}
                icon={Brain}
                trend={15}
                color="green"
              />
              <StatCard
                title="Defense Effectiveness"
                value={`${(realTimeData.defenseEffectiveness * 100).toFixed(1)}%`}
                icon={Shield}
                trend={3}
                color="blue"
              />
            </div>

            {/* Quick Actions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-8"
            >
              <h2 className="text-2xl font-bold text-white mb-6">Quick Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <button
                  onClick={() => setActiveTab('analyzer')}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-300 flex items-center space-x-3"
                >
                  <Brain className="w-6 h-6" />
                  <span>Analyze Smart Contract</span>
                </button>
                <button
                  onClick={() => setActiveTab('simulation')}
                  className="bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-300 flex items-center space-x-3"
                >
                  <Target className="w-6 h-6" />
                  <span>Start Attack Simulation</span>
                </button>
                <button
                  onClick={() => setActiveTab('wargames')}
                  className="bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-300 flex items-center space-x-3"
                >
                  <Users className="w-6 h-6" />
                  <span>Join War Game</span>
                </button>
              </div>
            </motion.div>

            {/* Recent Activity */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-8"
            >
              <h2 className="text-2xl font-bold text-white mb-6">Recent Activity</h2>
              <div className="space-y-4">
                {[
                  { time: '2 min ago', event: 'New threat pattern detected in DeFi protocol', severity: 'high' },
                  { time: '5 min ago', event: 'Smart contract analysis completed for 0x123...abc', severity: 'medium' },
                  { time: '8 min ago', event: 'Attack simulation finished with 3 vulnerabilities found', severity: 'high' },
                  { time: '12 min ago', event: 'Defense strategy updated for flash loan attacks', severity: 'low' },
                ].map((activity, index) => (
                  <div key={index} className="flex items-center space-x-4 p-4 bg-gray-700/30 rounded-lg">
                    <div className={`w-3 h-3 rounded-full ${
                      activity.severity === 'high' ? 'bg-red-400' :
                      activity.severity === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
                    }`} />
                    <div className="flex-1">
                      <p className="text-white">{activity.event}</p>
                      <p className="text-gray-400 text-sm">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        )
    }
  }

  return (
    <>
      <Head>
        <title>Quantum-AI Cyber God - Ultimate Web3 Defense System</title>
        <meta name="description" content="Decentralized cyber warfare simulator for Web3 security" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen">
        {/* Navigation */}
        <nav className="bg-gray-900/80 backdrop-blur-sm border-b border-gray-700 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-8">
                <div className="flex items-center space-x-2">
                  <Shield className="w-8 h-8 text-purple-400" />
                  <span className="text-xl font-bold text-white">Quantum-AI Cyber God</span>
                </div>
                
                <div className="hidden md:flex space-x-1">
                  {tabs.map((tab) => {
                    const Icon = tab.icon
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 ${
                          activeTab === tab.id
                            ? 'bg-purple-600 text-white'
                            : 'text-gray-300 hover:text-white hover:bg-gray-700'
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                        <span>{tab.label}</span>
                      </button>
                    )
                  })}
                </div>
              </div>

              <div className="flex items-center space-x-4">
                {isConnected && (
                  <div className="flex items-center space-x-2 text-green-400">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                    <span className="text-sm">Connected</span>
                  </div>
                )}
                <ConnectButton />
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {!isConnected ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-20"
            >
              <Shield className="w-24 h-24 text-purple-400 mx-auto mb-8" />
              <h1 className="text-4xl font-bold text-white mb-4">
                Connect Your Wallet to Begin
              </h1>
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                Access the most advanced Web3 security platform. Analyze smart contracts, 
                simulate attacks, and participate in cyber warfare games.
              </p>
              <ConnectButton />
            </motion.div>
          ) : (
            renderTabContent()
          )}
        </main>
      </div>
    </>
  )
} 