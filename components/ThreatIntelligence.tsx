import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle, Shield, Eye, Clock, TrendingUp } from 'lucide-react'

interface Threat {
  id: string
  type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  description: string
  timestamp: string
  source: string
  indicators: string[]
}

export default function ThreatIntelligence() {
  const [threats, setThreats] = useState<Threat[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate loading threats
    const loadThreats = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockThreats: Threat[] = [
        {
          id: '1',
          type: 'Flash Loan Attack',
          severity: 'critical',
          description: 'Suspicious flash loan activity detected targeting DeFi protocols',
          timestamp: new Date(Date.now() - 300000).toISOString(),
          source: 'AI Detection Engine',
          indicators: ['Large flash loan', 'Price manipulation', 'Arbitrage exploit']
        },
        {
          id: '2',
          type: 'Reentrancy Pattern',
          severity: 'high',
          description: 'Potential reentrancy attack pattern identified in smart contract',
          timestamp: new Date(Date.now() - 600000).toISOString(),
          source: 'Static Analysis',
          indicators: ['External call', 'State change after call', 'No reentrancy guard']
        },
        {
          id: '3',
          type: 'Phishing Campaign',
          severity: 'medium',
          description: 'New phishing campaign targeting Web3 wallet users',
          timestamp: new Date(Date.now() - 900000).toISOString(),
          source: 'Community Reports',
          indicators: ['Fake website', 'Social engineering', 'Wallet connection']
        }
      ]
      
      setThreats(mockThreats)
      setIsLoading(false)
    }

    loadThreats()
    
    // Simulate real-time updates
    const interval = setInterval(() => {
      if (Math.random() > 0.7) {
        const newThreat: Threat = {
          id: Date.now().toString(),
          type: 'New Threat Pattern',
          severity: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)] as any,
          description: 'AI detected new suspicious activity pattern',
          timestamp: new Date().toISOString(),
          source: 'Quantum AI Engine',
          indicators: ['Anomalous behavior', 'Pattern recognition']
        }
        setThreats(prev => [newThreat, ...prev.slice(0, 9)])
      }
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500/20 border-red-500 text-red-400'
      case 'high': return 'bg-orange-500/20 border-orange-500 text-orange-400'
      case 'medium': return 'bg-yellow-500/20 border-yellow-500 text-yellow-400'
      case 'low': return 'bg-green-500/20 border-green-500 text-green-400'
      default: return 'bg-gray-500/20 border-gray-500 text-gray-400'
    }
  }

  const formatTimeAgo = (timestamp: string) => {
    const diff = Date.now() - new Date(timestamp).getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(minutes / 60)
    
    if (hours > 0) return `${hours}h ago`
    return `${minutes}m ago`
  }

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <AlertTriangle className="w-16 h-16 text-red-400 mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-white mb-2">Threat Intelligence</h1>
        <p className="text-gray-300">Real-time monitoring of Web3 security threats</p>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Threats</p>
              <p className="text-2xl font-bold text-red-400">{threats.length}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-red-400" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Critical Alerts</p>
              <p className="text-2xl font-bold text-orange-400">
                {threats.filter(t => t.severity === 'critical').length}
              </p>
            </div>
            <Shield className="w-8 h-8 text-orange-400" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Detection Rate</p>
              <p className="text-2xl font-bold text-green-400">98.5%</p>
            </div>
            <Eye className="w-8 h-8 text-green-400" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Response Time</p>
              <p className="text-2xl font-bold text-blue-400">1.2s</p>
            </div>
            <Clock className="w-8 h-8 text-blue-400" />
          </div>
        </motion.div>
      </div>

      {/* Threat Feed */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-white">Live Threat Feed</h2>
          <div className="flex items-center space-x-2 text-green-400">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <span className="text-sm">Live</span>
          </div>
        </div>

        {isLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="bg-gray-700 h-20 rounded-lg" />
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {threats.map((threat, index) => (
              <motion.div
                key={threat.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`border rounded-lg p-4 ${getSeverityColor(threat.severity)}`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h3 className="font-semibold">{threat.type}</h3>
                      <span className="text-xs px-2 py-1 rounded-full bg-current/20 capitalize">
                        {threat.severity}
                      </span>
                    </div>
                    <p className="text-sm opacity-90 mb-2">{threat.description}</p>
                    <div className="flex items-center space-x-4 text-xs opacity-75">
                      <span>Source: {threat.source}</span>
                      <span>{formatTimeAgo(threat.timestamp)}</span>
                    </div>
                  </div>
                </div>
                
                {threat.indicators.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-current/20">
                    <p className="text-xs opacity-75 mb-1">Indicators:</p>
                    <div className="flex flex-wrap gap-1">
                      {threat.indicators.map((indicator, i) => (
                        <span
                          key={i}
                          className="text-xs px-2 py-1 bg-current/10 rounded"
                        >
                          {indicator}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  )
} 