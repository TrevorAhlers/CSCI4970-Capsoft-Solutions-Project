import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';

interface ClassMeeting {
  name: string;
  room: string;
  days: string[];
  startTime: string;
  endTime: string;
  instructor: string;
}

@Component({
  selector: 'app-class-view',
  templateUrl: './classroom.component.html',
  styleUrls: ['./classroom.component.scss'],
})
export class ClassComponent implements OnInit {
  classMeetings: ClassMeeting[] = [];
  rooms: string[] = [];
  timeSlots = [
    '08:00', '09:00',
    '10:00', '11:00',
    '12:00', '13:00',
    '14:00', '15:00',
    '16:00', '17:00','18:00',"19:00"
  ];
  daysOfWeek = [
    { key: 'Mon', label: 'M' },
    { key: 'Tue', label: 'T' },
    { key: 'Wed', label: 'W' },
    { key: 'Thu', label: 'Th' },
    { key: 'Fri', label: 'F' }
  ];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    const copiedCourse = this.dataService.getCourse();

    if (copiedCourse?.content) {
      const extractedMeetings = this.extractMeetingsFromHtml(copiedCourse.content);
      this.classMeetings = extractedMeetings;
      this.rooms = [...new Set(extractedMeetings.map(m => m.room))];
    }
  }

  extractMeetingsFromHtml(html: string): ClassMeeting[] {
    const meetings: ClassMeeting[] = [];

    const scheduleMatch = html.match(/Schedule:\s*\[(.*?)\]/);
    const scheduleStr = scheduleMatch ? scheduleMatch[1] : '';

    const scheduleEntries = Array.from(scheduleStr.matchAll(/\('(.*?)',\s*'(.*?)',\s*'(.*?)',\s*(\d+),\s*(\d+)\)/g));
    const courseName = this.extractField(html, 'Course');
    const instructor = this.extractField(html, 'Instructor');
    const mergedMeetings: any[] = [];

    for (const match of scheduleEntries) {
      const [_, name, room, day, start, end] = match;

      const startTime = this.convertMinutesToTime(+start);
      const endTime = this.convertMinutesToTime(+end);

      const existing = mergedMeetings.find(
        (m) =>
          m.name === (courseName || name) &&
          m.room === room.trim() &&
          m.startTime === startTime &&
          m.endTime === endTime &&
          m.instructor === instructor
      );

      if (existing) {
        existing.days.push(day);
      } else {
        mergedMeetings.push({
          name: courseName || name,
          room: room.trim(),
          days: [day],
          startTime,
          endTime,
          instructor,
        });
      }
    }

    return mergedMeetings;
  }

  extractField(html: string, label: string): string {
    const match = html.match(new RegExp(`<p>${label}:\\s*(.*?)</p>`));
    return match ? match[1].trim() : '';
  }

  convertMinutesToTime(mins: number): string {
    const hours = Math.floor(mins / 60);
    const minutes = mins % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  }

  getClassAt(room: string, time: string, ): ClassMeeting | null {
    return this.classMeetings.find(meeting =>
      meeting.room === room &&
      time >= meeting.startTime &&
      time < meeting.endTime
    ) || null;
  }

  isClassStart(meeting: ClassMeeting, time: string): boolean {
    return meeting.startTime === time;
  }

  getSlotSpan(start: string, end: string): number {
	const toMinutes = (t: string): number => {
	  const [h, m] = t.split(':').map(Number);
	  return (h * 60) + m;
	};
  
	const startMinutes = toMinutes(start);
	const endMinutes = toMinutes(end);
	
	
	const spanInMinutes = endMinutes - startMinutes;
	const span = Math.ceil((toMinutes(end) - toMinutes(start)) / 60);
	return span;
  }
  

  formatTimeTo24Hour(time: number): string {
    const hour = Math.floor(time / 100);
    const minutes = time % 100;
    const hours24 = hour < 12 ? hour : (hour === 12 ? hour : hour - 12);
    const minutesFormatted = minutes < 10 ? `0${minutes}` : minutes;
    return `${hours24}:${minutesFormatted}`;
  }
  
  
}
