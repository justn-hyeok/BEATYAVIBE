document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("searchButton");
  const artistInput = document.getElementById("artist");
  const results = document.getElementById("results");
  const error = document.getElementById("error");

  // 에러 메시지 표시 함수
  const displayError = (message) => {
    error.textContent = message;
    error.classList.remove("d-none");
  };

  // 에러 메시지 초기화 함수
  const clearError = () => {
    error.textContent = "";
    error.classList.add("d-none");
  };

  // 검색 결과 초기화 함수
  const clearResults = () => {
    results.innerHTML = "";
  };

  // 아티스트의 곡을 가져오는 함수
  const fetchSongs = async (artist) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/search?artist=${encodeURIComponent(artist)}`);
      const data = await response.json();

      if (data.results && data.results.length > 0) {
        data.results.forEach((song) => {
          const li = document.createElement("li");
          li.innerHTML = `<strong>${song.name}</strong> by ${song.artist} - <a href="${song.url}" target="_blank">Listen</a>`;
          results.appendChild(li);
        });
      } else {
        displayError("No songs found for this artist.");
      }
    } catch (err) {
      displayError("An error occurred while searching.");
    }
  };

  // 검색 버튼 클릭 시 실행되는 함수
  const handleSearch = () => {
    const artist = artistInput.value.trim();
    clearResults();
    clearError();

    if (!artist) {
      displayError("Please enter an artist name.");
      return;
    }

    fetchSongs(artist);
  };

  // 검색 버튼 클릭 이벤트 리스너
  searchButton.addEventListener("click", handleSearch);

  // Enter 키 입력 시 검색 실행
  artistInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSearch();
    }
  });
});