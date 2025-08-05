import { authApi } from '@/lib/api'

export async function getReports() {
  return authApi.get('/reports/')
}

export async function getReport(reportId) {
  return authApi.get(`/reports/${reportId}`)
}

export async function applyReport(reportId) {
  return authApi.get(`/reports/${reportId}/apply`)
}

export async function rejectReport(reportId) {
  return authApi.get(`/reports/${reportId}/reject`)
}

export async function confirmReport(reportId) {
  return authApi.get(`/reports/${reportId}/confirm`)
}

export async function issueReport(reportId) {
  return authApi.get(`/reports/${reportId}/issue`)
}

export async function closeReport(reportId) {
  return authApi.get(`/reports/${reportId}/close`)
}

export async function getTickets(reportId) {
  return authApi.get(`/reports/${reportId}/tickets`)
}

export async function getTicket(ticketId) {
  return authApi.get(`/tickets/${ticketId}`)
}
