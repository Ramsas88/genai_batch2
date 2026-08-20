
# properties file 

spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB

app.upload.directory=uploads

# controller class

@PostMapping(value = "/upload",consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
public ResponseEntity<FileUploadResponse> uploadPdf(@RequestParam("file") MultipartFile file) {

    FileUploadResponse response = fileStorageService.uploadPdf(file);

    return ResponseEntity.status(HttpStatus.CREATED).body(response);
}

# service class

public FileUploadResponse uploadPdf(MultipartFile file) {

    if (file == null || file.isEmpty()) {
        throw new FileStorageException("Please select a PDF file");
    }

    if (file.getSize() > MAX_FILE_SIZE) {
        throw new FileStorageException(
                "File size must not exceed 10 MB"
        );
    }

    String originalFileName = file.getOriginalFilename();

    if (originalFileName == null
            || !originalFileName.toLowerCase(Locale.ROOT).endsWith(".pdf")) {
        throw new FileStorageException("Only .pdf files are allowed");
    }

    if (!PDF_CONTENT_TYPE.equalsIgnoreCase(file.getContentType())) {
        throw new FileStorageException(
                "Invalid content type. Only application/pdf is allowed"
        );
    }


    String storedFileName = UUID.randomUUID() + ".pdf";
    Path destination = uploadDirectory.resolve(storedFileName).normalize();

    
}

