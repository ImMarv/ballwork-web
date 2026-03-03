export async function search(query: string): Promise<string[]> {
    // Temporary mock data for UI demo
    const mockData = [
      "Lionel Messi",
      "Cristiano Ronaldo",
      "Kylian Mbappé",
      "Erling Haaland",
      "Manchester City",
      "Real Madrid"
    ];
  
    return mockData.filter(item =>
      item.toLowerCase().includes(query.toLowerCase())
    );
  }