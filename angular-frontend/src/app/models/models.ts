export interface ZoneDto {
  id: number;
  name: string;
  valveState: string;
}
export interface ReadingDto {
  waterLevel: number;
  recordedAt: string;
}
export interface AlertDto {
  id: number;
  zoneName: string;
  severity: string;
  geminiExplanation: string;
  priority: number;
  recommendedAction: string;
  ticketId: number;
  ticketStatus: string;
}
export interface ComplaintDto {
  zoneId: number;
  description: string;
  category: string;
  priority: string;
}
export interface AuthDto {
  username: string;
  role: string;
}