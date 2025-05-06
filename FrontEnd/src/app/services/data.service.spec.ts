import { TestBed } from '@angular/core/testing';
import { DataService } from './data.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('DataService', () => {
  let service: DataService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DataService],
    });

    service = TestBed.inject(DataService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTestingController.verify(); 
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get data', () => {
    const mockData = "";
     
    expect(service.getData()).toBeTruthy()
    service.getData().subscribe((data) => {
      expect(data).toBe(mockData);
      close();
    });

    const httpRequest = httpTestingController.expectOne('http://localhost:5000/api/data');
    expect(httpRequest.request.method).toBe('GET');
    
   
  });
});
