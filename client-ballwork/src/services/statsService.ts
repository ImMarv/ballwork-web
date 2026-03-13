import { api } from "./apiClient"

export const statsService = {

  async unifiedSearch(query: string) {
    const response = await api.get("/search", {
      params: { query }
    })
    return response.data
  },

  async searchPlayers(query: string, limit: number) {
    const response = await api.get("/search/player", {
      params: { query, limit }
    })
    return response.data
  },

  async searchTeams(query: string, limit: number) {
    const response = await api.get("/search/team", {
      params: { query, limit }
    })
    return response.data
  },

  async searchCompetitions(query: string, limit: number) {
    const response = await api.get("/search/competition", {
      params: { query, limit }
    })
    return response.data
  },

  async getPlayer(playerId: number, year?: string) {
    const response = await api.get(`/player/${playerId}`, {
      params: { year }
    })
    return response.data
  },

  async getTeam(teamId: number, competitionId?: number, year?: string) {
    const response = await api.get(`/team/${teamId}`, {
      params: {
        competition_id: competitionId,
        year
      }
    })
    return response.data
  },

  async getCompetition(competitionId: number) {
    const response = await api.get("/competition", {
      params: { competition_id: competitionId }
    })
    return response.data
  },

  async getCountry(countryCode: string) {
    const response = await api.get("/country", {
      params: { country_code: countryCode }
    })
    return response.data
  }

}