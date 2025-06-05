#!/usr/bin/env python3
"""
Minimal test script to debug Semantic Scholar API behavior
Testing the hypotheses about pagination, year filtering, and query configuration
"""

import requests
import json
import time
from datetime import datetime

def test_raw_api_call(query, year_filter=None, limit=10, offset=0, fields=None):
    """
    Make a direct API call to Semantic Scholar to test behavior
    """
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    # Default fields to request
    if fields is None:
        fields = "paperId,title,authors,year,abstract,citationCount,venue,externalIds"
    
    params = {
        "query": query,
        "limit": limit,
        "offset": offset,
        "fields": fields
    }
    
    # Add year filter if specified
    if year_filter:
        params["year"] = year_filter
    
    print(f"\n🔍 Testing API call:")
    print(f"   URL: {base_url}")
    print(f"   Query: '{query}'")
    print(f"   Year filter: {year_filter}")
    print(f"   Limit: {limit}, Offset: {offset}")
    print(f"   Fields: {fields}")
    
    try:
        response = requests.get(base_url, params=params)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response URL: {response.url}")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            papers = data.get("data", [])
            
            print(f"   Total available: {total}")
            print(f"   Papers returned: {len(papers)}")
            
            if papers:
                print(f"\n📚 Sample papers:")
                for i, paper in enumerate(papers[:3]):  # Show first 3
                    print(f"     {i+1}. Title: {paper.get('title', 'No title')[:80]}...")
                    print(f"        Paper ID: {paper.get('paperId', 'No ID')}")
                    print(f"        Year: {paper.get('year', 'No year')}")
                    print(f"        Authors: {[a.get('name', '') for a in paper.get('authors', [])]}")
                    print(f"        Citations: {paper.get('citationCount', 0)}")
                    print(f"        Abstract available: {'Yes' if paper.get('abstract') else 'No'}")
                    if paper.get('abstract'):
                        print(f"        Abstract preview: {paper.get('abstract', '')[:100]}...")
                    print()
            
            return {
                "success": True,
                "total": total,
                "papers": papers,
                "raw_response": data
            }
        else:
            print(f"   Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text
            }
            
    except Exception as e:
        print(f"   Exception: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def test_pagination(query, year_filter=None, max_pages=3):
    """
    Test pagination behavior to see if we get different results
    """
    print(f"\n🔄 Testing pagination for query: '{query}'")
    all_paper_ids = set()
    
    for page in range(max_pages):
        offset = page * 10  # 10 results per page
        print(f"\n   Page {page + 1} (offset={offset}):")
        
        result = test_raw_api_call(query, year_filter, limit=10, offset=offset)
        
        if result["success"]:
            papers = result["papers"]
            if not papers:
                print(f"   No more papers found at offset {offset}")
                break
                
            page_paper_ids = {p.get('paperId', '') for p in papers}
            overlap = all_paper_ids.intersection(page_paper_ids)
            
            print(f"   Papers on this page: {len(papers)}")
            print(f"   New unique papers: {len(page_paper_ids - all_paper_ids)}")
            print(f"   Duplicates from previous pages: {len(overlap)}")
            
            all_paper_ids.update(page_paper_ids)
        else:
            print(f"   Failed to get page {page + 1}")
            break
        
        # Rate limiting
        time.sleep(2)
    
    print(f"\n📊 Pagination Summary:")
    print(f"   Total unique papers found: {len(all_paper_ids)}")
    return all_paper_ids

def main():
    """
    Main testing function implementing the debugging strategy
    """
    print("=" * 80)
    print("🔍 SEMANTIC SCHOLAR API DEBUG SESSION")
    print(f"🕒 Started at: {datetime.now()}")
    print("=" * 80)
    
    # Test queries from simple to complex
    test_queries = [
        "supply chain agent",
        "agent scm", 
        "autonomous agent logistics",
        "agent-based supply chain",
        "multi-agent supply chain"
    ]
    
    print("\n" + "=" * 50)
    print("📝 HYPOTHESIS 1: YEAR FILTERING ISSUES")
    print("=" * 50)
    
    # Test 1: No year filter
    print("\n🧪 Test 1.1: No year filter (should return many results)")
    result_no_year = test_raw_api_call("supply chain agent", year_filter=None, limit=20)
    
    time.sleep(3)
    
    # Test 2: 2025 only
    print("\n🧪 Test 1.2: Year 2025 only")
    result_2025 = test_raw_api_call("supply chain agent", year_filter="2025", limit=20)
    
    time.sleep(3)
    
    # Test 3: Broader range 2024-2025
    print("\n🧪 Test 1.3: Year range 2024-2025")
    result_2024_2025 = test_raw_api_call("supply chain agent", year_filter="2024-2025", limit=20)
    
    time.sleep(3)
    
    print("\n" + "=" * 50)
    print("📝 HYPOTHESIS 2: PAGINATION ISSUES")
    print("=" * 50)
    
    # Test pagination with no year filter
    print("\n🧪 Test 2.1: Pagination test (no year filter)")
    unique_papers_no_year = test_pagination("supply chain agent", year_filter=None, max_pages=3)
    
    time.sleep(3)
    
    # Test pagination with 2025 filter
    print("\n🧪 Test 2.2: Pagination test (2025 only)")
    unique_papers_2025 = test_pagination("supply chain agent", year_filter="2025", max_pages=3)
    
    print("\n" + "=" * 50)
    print("📝 HYPOTHESIS 3: QUERY DIVERSITY")
    print("=" * 50)
    
    # Test multiple queries without year filter
    print("\n🧪 Test 3.1: Multiple queries without year filter")
    all_unique_papers = set()
    
    for i, query in enumerate(test_queries):
        print(f"\n   Testing query {i+1}: '{query}'")
        result = test_raw_api_call(query, year_filter=None, limit=10)
        
        if result["success"]:
            paper_ids = {p.get('paperId', '') for p in result["papers"]}
            overlap = all_unique_papers.intersection(paper_ids)
            
            print(f"   Unique papers from this query: {len(paper_ids)}")
            print(f"   New papers not seen before: {len(paper_ids - all_unique_papers)}")
            print(f"   Overlap with previous queries: {len(overlap)}")
            
            all_unique_papers.update(paper_ids)
        
        time.sleep(3)
    
    print(f"\n📊 Query Diversity Summary:")
    print(f"   Total unique papers across all queries: {len(all_unique_papers)}")
    
    print("\n" + "=" * 50)
    print("📝 HYPOTHESIS 4: FIELD CONFIGURATION")
    print("=" * 50)
    
    # Test with minimal fields
    print("\n🧪 Test 4.1: Minimal fields (paperId, title)")
    result_minimal = test_raw_api_call("supply chain agent", 
                                     year_filter=None, 
                                     limit=10, 
                                     fields="paperId,title")
    
    time.sleep(3)
    
    # Test with all fields
    print("\n🧪 Test 4.2: All available fields")
    result_full = test_raw_api_call("supply chain agent", 
                                  year_filter=None, 
                                  limit=10, 
                                  fields="paperId,title,authors,year,abstract,citationCount,venue,externalIds,referenceCount,influentialCitationCount,isOpenAccess,openAccessPdf,publicationTypes,publicationDate")
    
    print("\n" + "=" * 80)
    print("🎯 SUMMARY AND CONCLUSIONS")
    print("=" * 80)
    
    print(f"\n📊 Results Summary:")
    if result_no_year["success"]:
        print(f"   No year filter: {result_no_year['total']} total papers available")
    if result_2025["success"]:
        print(f"   2025 only: {result_2025['total']} total papers available")
    if result_2024_2025["success"]:
        print(f"   2024-2025: {result_2024_2025['total']} total papers available")
    
    print(f"   Unique papers from pagination test (no year): {len(unique_papers_no_year) if 'unique_papers_no_year' in locals() else 'N/A'}")
    print(f"   Unique papers from pagination test (2025): {len(unique_papers_2025) if 'unique_papers_2025' in locals() else 'N/A'}")
    print(f"   Unique papers across diverse queries: {len(all_unique_papers)}")
    
    print(f"\n🔍 Key Findings:")
    
    # Year filter analysis
    if result_no_year["success"] and result_2025["success"]:
        no_year_total = result_no_year["total"]
        year_2025_total = result_2025["total"]
        
        if no_year_total > year_2025_total * 10:
            print(f"   ✅ Year filtering appears to be working (significant reduction: {no_year_total} → {year_2025_total})")
        elif year_2025_total == 0:
            print(f"   ❌ Year 2025 filter returns zero results - this may be the issue!")
        elif year_2025_total == 1:
            print(f"   ⚠️ Year 2025 filter returns only 1 result - very restrictive!")
        else:
            print(f"   ⚠️ Year filtering may be working but very restrictive ({no_year_total} → {year_2025_total})")
    
    # Pagination analysis
    if 'unique_papers_no_year' in locals() and 'unique_papers_2025' in locals():
        if len(unique_papers_no_year) > 10:
            print(f"   ✅ Pagination appears to be working (got {len(unique_papers_no_year)} unique papers)")
        else:
            print(f"   ❌ Pagination may not be working properly (only {len(unique_papers_no_year)} unique papers)")
        
        if len(unique_papers_2025) <= 1:
            print(f"   ❌ 2025 pagination confirms very few results ({len(unique_papers_2025)} papers)")
    
    # Query diversity analysis
    if len(all_unique_papers) > len(test_queries):
        print(f"   ✅ Query diversity working (different queries return different results)")
    else:
        print(f"   ❌ Query diversity issues (queries may be returning same results)")
    
    print(f"\n🎯 Next Steps Based on Results:")
    
    if result_2025["success"] and result_2025["total"] <= 1:
        print(f"   1. 🔴 CRITICAL: Year 2025 filter is too restrictive or malfunctioning")
        print(f"   2. 📅 Use broader year range (2024-2025) or no year filter")
        print(f"   3. 🔍 Investigate why Semantic Scholar has so few 2025 papers")
    
    if len(all_unique_papers) <= len(test_queries):
        print(f"   1. 🔴 Query diversity issue - investigate query syntax")
        print(f"   2. 🔧 Check if API endpoint is correct")
        print(f"   3. 📄 Verify pagination parameters")
    
    print(f"\n🕒 Debug session completed at: {datetime.now()}")
    print("=" * 80)

if __name__ == "__main__":
    main()
