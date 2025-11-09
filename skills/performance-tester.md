---
name: performance-tester
description: Creates performance and load tests for document processing pipelines using pytest-benchmark and pytest-memray. Tests large document handling, memory usage, batch processing, and parser performance. Invoke when testing performance or validating scalability.
---

# Performance Tester

Specialized performance testing for data ingestion pipelines with emphasis on large document processing, memory efficiency, benchmark validation, and scalability testing.

## Core Responsibilities

- **Benchmark Testing**: Parser performance comparison, chunking speed, export efficiency
- **Memory Profiling**: Memory usage validation with pytest-memray
- **Large Document Testing**: Processing multi-hundred page documents
- **Batch Processing**: Concurrent document processing performance
- **Regression Prevention**: Performance regression detection

## Performance Testing Approach

### Benchmark Testing with pytest-benchmark

**Parser Performance Benchmarking**:
```python
@pytest.mark.perf
class TestParserPerformance:
    """Benchmark parser performance."""

    def test_pymupdf_parser_benchmark(self, benchmark, temp_test_file):
        """Benchmark PyMuPDF parser performance."""
        parser = PyMuPDFParser()
        doc = Document(
            source_path=temp_test_file,
            format=DocumentFormat.PDF,
            status=ProcessingStatus.PENDING,
        )

        # Benchmark the parsing operation
        result = benchmark(parser.parse, doc)

        # Assert performance criteria
        assert result.success is True
        # Benchmark automatically captures timing statistics

    def test_chunking_performance_benchmark(self, benchmark, sample_large_document):
        """Benchmark chunking strategy performance."""
        chunker = TokenChunker(chunk_size=1000, chunk_overlap=200)

        # Benchmark chunking operation
        chunks = benchmark(chunker.chunk_document, sample_large_document)

        assert len(chunks) > 0

    @pytest.mark.parametrize("parser_class,priority", [
        (PyMuPDFParser, "baseline"),
        (PyMuPDF4LLMParser, "enhanced"),
        (MarkerPDFParser, "premium"),
    ])
    def test_parser_comparison_benchmark(self, benchmark, temp_test_file, parser_class, priority):
        """Compare parser performance across implementations."""
        parser = parser_class()
        doc = Document(source_path=temp_test_file, format=DocumentFormat.PDF)

        result = benchmark(parser.parse, doc)

        # Results stored for comparison in .benchmarks/
        assert result.success is True
```

**Export Performance**:
```python
@pytest.mark.perf
def test_json_export_performance(benchmark, sample_large_document):
    """Benchmark JSON export performance."""
    exporter = DocumentExporter()

    # Benchmark export operation
    json_data = benchmark(exporter.to_json, sample_large_document)

    assert "document_id" in json_data

@pytest.mark.perf
def test_markdown_export_performance(benchmark, sample_large_document):
    """Benchmark Markdown export performance."""
    exporter = DocumentExporter()

    markdown = benchmark(exporter.to_markdown, sample_large_document)

    assert markdown is not None
```

### Memory Profiling with pytest-memray

**Memory Usage Validation**:
```python
@pytest.mark.perf
@pytest.mark.limit_memory("100 MB")
def test_parser_memory_usage(tmp_path):
    """Test that PDF parsing stays within memory limits."""
    # Create realistic 50-page PDF
    pdf_file = create_large_pdf(tmp_path, pages=50)

    parser = PyMuPDFParser()
    doc = Document(source_path=pdf_file, format=DocumentFormat.PDF)

    # Parse document (memray tracks memory)
    result = parser.parse(doc)

    assert result.success is True
    # pytest-memray will fail test if > 100 MB used

@pytest.mark.perf
@pytest.mark.limit_memory("500 MB")
def test_large_document_chunking_memory(tmp_path):
    """Test chunking memory efficiency with large documents."""
    # Create document with 10,000 elements
    doc = create_document_with_many_elements(element_count=10_000)

    chunker = TokenChunker(chunk_size=1000)

    # Chunk document (memory tracked)
    chunks = chunker.chunk_document(doc)

    assert len(chunks) > 0
```

**Memory Leak Detection**:
```python
@pytest.mark.perf
def test_no_memory_leaks_in_batch_processing(tmp_path):
    """Test that batch processing doesn't leak memory."""
    import gc
    import tracemalloc

    tracemalloc.start()
    initial_snapshot = tracemalloc.take_snapshot()

    # Process 100 documents
    for i in range(100):
        pdf_file = create_small_pdf(tmp_path / f"doc_{i}.pdf")
        parser = PyMuPDFParser()
        doc = Document(source_path=pdf_file, format=DocumentFormat.PDF)
        result = parser.parse(doc)
        del result
        del doc
        gc.collect()

    final_snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()

    # Compare memory usage
    stats = final_snapshot.compare_to(initial_snapshot, 'lineno')

    # Total memory increase should be minimal (< 10 MB)
    total_increase = sum(stat.size_diff for stat in stats) / (1024 * 1024)
    assert total_increase < 10, f"Memory leak detected: {total_increase} MB increase"
```

### Large Document Testing

**Scalability Validation**:
```python
@pytest.mark.perf
@pytest.mark.slow
@pytest.mark.parametrize("page_count,max_duration", [
    (10, 5.0),    # 10 pages in < 5 seconds
    (50, 20.0),   # 50 pages in < 20 seconds
    (100, 40.0),  # 100 pages in < 40 seconds
])
def test_large_document_processing_time(tmp_path, page_count, max_duration, performance_metrics):
    """Test processing time scales linearly with document size."""
    # Create large PDF
    pdf_file = create_large_pdf(tmp_path, pages=page_count)

    router = DocumentRouter(Settings())
    router.parser_registry.register(PyMuPDFParser(), [DocumentFormat.PDF])

    # Measure processing time
    performance_metrics.start()
    document, result = router.process_document(source_path=pdf_file)
    performance_metrics.stop()

    # Verify success and performance
    assert result.success is True
    performance_metrics.assert_max_duration(max_duration)

@pytest.mark.perf
@pytest.mark.slow
def test_processes_1000_page_document(tmp_path):
    """Test that very large documents can be processed."""
    # Create 1000-page PDF
    large_pdf = create_large_pdf(tmp_path, pages=1000)

    parser = PyMuPDFParser()
    doc = Document(source_path=large_pdf, format=DocumentFormat.PDF)

    # Should complete without crashing
    result = parser.parse(doc)

    assert result.success is True
    assert len(result.elements) > 100  # Should extract significant content
```

**Element Count Scalability**:
```python
@pytest.mark.perf
@pytest.mark.parametrize("element_count", [100, 1_000, 10_000, 100_000])
def test_chunking_scales_with_element_count(element_count):
    """Test that chunking performance scales with element count."""
    import time

    doc = create_document_with_many_elements(element_count)
    chunker = TokenChunker(chunk_size=1000)

    start = time.perf_counter()
    chunks = chunker.chunk_document(doc)
    duration = time.perf_counter() - start

    # Should scale roughly linearly (allow 2x factor)
    expected_duration = element_count / 10_000  # Baseline: 10k elements in 1 second
    assert duration < expected_duration * 2, f"Chunking too slow: {duration}s for {element_count} elements"
```

### Batch Processing Performance

**Concurrent Processing**:
```python
@pytest.mark.perf
def test_batch_processing_performance(tmp_path):
    """Test batch processing of multiple documents."""
    import time

    # Create 20 test documents
    pdf_files = [
        create_realistic_pdf(tmp_path / f"doc_{i}.pdf", pages=5)
        for i in range(20)
    ]

    router = DocumentRouter(Settings())
    router.parser_registry.register(PyMuPDFParser(), [DocumentFormat.PDF])

    # Process batch
    start = time.perf_counter()
    results = []
    for pdf_file in pdf_files:
        doc, result = router.process_document(source_path=pdf_file)
        results.append(result)
    duration = time.perf_counter() - start

    # Verify all succeeded
    assert all(r.success for r in results)

    # Should complete in reasonable time (< 1 second per document on average)
    average_duration = duration / len(pdf_files)
    assert average_duration < 1.0, f"Batch processing too slow: {average_duration}s per document"

@pytest.mark.perf
def test_parallel_processing_benefit(tmp_path):
    """Test that parallel processing improves throughput."""
    import time
    from concurrent.futures import ThreadPoolExecutor

    pdf_files = [
        create_realistic_pdf(tmp_path / f"doc_{i}.pdf", pages=5)
        for i in range(10)
    ]

    router = DocumentRouter(Settings())
    router.parser_registry.register(PyMuPDFParser(), [DocumentFormat.PDF])

    # Sequential processing
    start_seq = time.perf_counter()
    for pdf_file in pdf_files:
        router.process_document(source_path=pdf_file)
    sequential_duration = time.perf_counter() - start_seq

    # Parallel processing
    start_par = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(router.process_document, source_path=pdf_file)
            for pdf_file in pdf_files
        ]
        results = [f.result() for f in futures]
    parallel_duration = time.perf_counter() - start_par

    # Parallel should be faster (at least 1.5x speedup)
    speedup = sequential_duration / parallel_duration
    assert speedup > 1.5, f"Insufficient parallel speedup: {speedup}x"
```

### Performance Regression Testing

**Baseline Comparison**:
```python
@pytest.mark.perf
def test_parser_performance_regression(benchmark, temp_test_file):
    """Test that parser performance hasn't regressed."""
    parser = PyMuPDFParser()
    doc = Document(source_path=temp_test_file, format=DocumentFormat.PDF)

    # Benchmark will compare against previous runs in .benchmarks/
    result = benchmark(parser.parse, doc)

    # pytest-benchmark will fail if performance regressed > 5% (configurable)
    assert result.success is True
```

**Performance Criteria**:
```python
@pytest.mark.perf
class TestPerformanceCriteria:
    """Test that performance criteria are met."""

    def test_small_pdf_parsing_under_1_second(self, tmp_path):
        """Test that small PDFs parse in under 1 second."""
        import time

        pdf_file = create_small_pdf(tmp_path, pages=5)
        parser = PyMuPDFParser()
        doc = Document(source_path=pdf_file, format=DocumentFormat.PDF)

        start = time.perf_counter()
        result = parser.parse(doc)
        duration = time.perf_counter() - start

        assert result.success is True
        assert duration < 1.0, f"Parsing too slow: {duration}s"

    def test_chunking_1000_elements_under_100ms(self):
        """Test that chunking 1000 elements completes in < 100ms."""
        import time

        doc = create_document_with_many_elements(1000)
        chunker = TokenChunker(chunk_size=500)

        start = time.perf_counter()
        chunks = chunker.chunk_document(doc)
        duration = time.perf_counter() - start

        assert len(chunks) > 0
        assert duration < 0.1, f"Chunking too slow: {duration}s"
```

## Performance Test Fixtures

**Large Document Fixtures**:
```python
@pytest.fixture
def sample_large_document():
    """Create a large document with many elements for performance testing."""
    doc = Document(
        document_id="perf-test-large",
        source_path=None,
        format=DocumentFormat.PDF,
        status=ProcessingStatus.COMPLETED,
    )

    # Create 1000 elements
    doc.elements = [
        DocumentElement(
            element_type=ElementType.NARRATIVE_TEXT,
            content=f"Performance test paragraph {i} with some content.",
            metadata=ElementMetadata(page_number=(i // 100) + 1),
        )
        for i in range(1000)
    ]

    return doc

@pytest.fixture
def performance_metrics():
    """Provide performance measurement utility."""
    from tests.conftest import PerformanceMetrics
    return PerformanceMetrics(max_duration=5.0)
```

## Performance Test Markers

**Required Markers**:
```python
@pytest.mark.perf  # Performance test
@pytest.mark.slow  # Excluded from fast dev cycle
@pytest.mark.benchmark  # Uses pytest-benchmark
```

## Integration Points

- **pytest-benchmark** - Automated performance benchmarking
- **pytest-memray** - Memory profiling and leak detection
- **performance_metrics fixture** - Custom timing utilities
- **.benchmarks/** directory - Historical benchmark data

## Output Standards

**Performance Test Quality**:
- Clear performance criteria
- Baseline expectations documented
- Regression prevention via benchmarks
- Memory limits specified

**Benchmark Configuration**:
```python
# In pyproject.toml
[tool.pytest.benchmark]
min_rounds = 5
max_time = 1.0
calibration_precision = 10
compare_fail = ["min:5%", "max:5%", "mean:5%"]
```

**Test Documentation**:
```python
@pytest.mark.perf
def test_performance_scenario(benchmark):
    """
    Test [performance aspect].

    Performance Criteria:
    - Operation should complete in < X seconds
    - Memory usage should be < Y MB
    - Throughput should be > Z items/second
    """
```

---

*Use this skill when: testing performance, validating scalability, detecting memory leaks, comparing parser performance, preventing regressions*
