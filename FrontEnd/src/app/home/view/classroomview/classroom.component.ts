import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';

interface ClassMeeting {
	name: string;
	room: string;
	days: string[];
	startTime: string;
	endTime: string;
	instructor: string;
	rawstartTime: string;
	rawendTime: string;
	rawMeetingText?: string;
}

@Component({
	selector: 'app-class-view',
	templateUrl: './classroom.component.html',
	styleUrls: ['./classroom.component.scss'],
})
export class ClassComponent implements OnInit {
	classMeetings: ClassMeeting[] = [];

	timeSlots = [
		'08:00', '08:30', '09:00', '09:30',
		'10:00', '10:30', '11:00', '11:30',
		'12:00', '12:30', '13:00', '13:30',
		'14:00', '14:30', '15:00', '15:30',
		'16:00', '16:30', '17:00', '17:00',
		'18:00', '18:30'
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
		}
	}

	extractMeetingsFromHtml(html: string): ClassMeeting[] {
		const dayMap: { [key: string]: string } = {
			M: 'Mon',
			T: 'Tue',
			W: 'Wed',
			R: 'Thu',
			F: 'Fri'
		};

		const meetings: ClassMeeting[] = [];

		const scheduleMatch = html.match(/Schedule:\s*\[(.*?)\]/);
		const scheduleStr = scheduleMatch ? scheduleMatch[1] : '';

		const rawMeetingMatch = html.match(/Meetings:\s*(.*?)(<br>|<\/p>|\n|$)/i);
		const rawMeetingText = rawMeetingMatch ? rawMeetingMatch[1].trim() : '';

		const entries = Array.from(scheduleStr.matchAll(/\('(.*?)',\s*'(.*?)',\s*'(.*?)',\s*(\d+),\s*(\d+)\)/g));
		const courseName = this.extractField(html, 'Course');
		const instructor = this.extractField(html, 'Instructor');
		const merged: any[] = [];

		for (const match of entries) {
			const [_, name, room, day, start, end] = match;
			const dayKey = dayMap[day] ?? day;
			const startTime = this.convertMinutesToTime(+start);
			const endTime = this.convertMinutesToTime(+end);
			const rawstartTime = start;
			const rawendTime = end;

			const existing = merged.find(m =>
				m.name === (courseName || name) &&
				m.room === room &&
				m.startTime === startTime &&
				m.endTime === endTime &&
				m.instructor === instructor
			);

			if (existing) {
				existing.days.push(dayKey);
			} else {
				merged.push({
					name: courseName || name,
					room: room.trim(),
					days: [dayKey],
					startTime,
					endTime,
					instructor,
					rawstartTime,
					rawendTime,
					rawMeetingText
				});
			}
		}

		return merged;
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

	getClassAt(dayKey: string, time: string): ClassMeeting | null {
		return this.classMeetings.find(meeting =>
			meeting.days.includes(dayKey) &&
			time >= meeting.startTime &&
			time < meeting.endTime
		) || null;
	}

	isClassStart(meeting: ClassMeeting, time: string): boolean {
		return meeting.startTime === time;
	}

	getSlotSpan(start: string, end: string): number {
		const toMinutes = (t: string) => {
			const [h, m] = t.split(':').map(Number);
			return h * 60 + m;
		};

		const startMinutes = toMinutes(start);
		const endMinutes = toMinutes(end);
		let startSlotIndex = Math.floor(startMinutes / 60);
		const startFraction = startMinutes % 60;

		if (startFraction !== 0) {
			startSlotIndex += 1;
		}

		const duration = Math.ceil((endMinutes - startMinutes) / 60);
		return duration;
	}
}
