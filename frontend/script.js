document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("searchButton");
  const randomButton = document.getElementById("randomButton");
  const artistInput = document.getElementById("artist");
  const results = document.getElementById("results");
  const error = document.getElementById("error");
  const themeToggle = document.getElementById("themeToggle");
  const moonIcon = themeToggle.querySelector("i");

  // 초기 테마 설정 (localStorage 사용)
  const savedTheme = localStorage.getItem("theme") || "dark";
  document.body.classList.add(savedTheme);
  updateThemeIcon(savedTheme);

  // 테마 전환 버튼 클릭 이벤트
  themeToggle.addEventListener("click", () => {
    const currentTheme = document.body.classList.contains("dark") ? "dark" : "light";
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    // 테마 변경
    document.body.classList.remove(currentTheme);
    document.body.classList.add(newTheme);

    // localStorage에 저장
    localStorage.setItem("theme", newTheme);

    // 아이콘 업데이트
    updateThemeIcon(newTheme);
  });

  // 아이콘 업데이트 함수
  function updateThemeIcon(theme) {
    moonIcon.className = theme === "dark" ? "fas fa-moon" : "fas fa-sun";
  }

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
        return data.results; // 곡 리스트 반환
      } else {
        displayError("No songs found for this artist.");
        return [];
      }
    } catch (err) {
      displayError("An error occurred while searching.");
      return [];
    }
  };

  // 검색 결과 표시 함수
  const displaySongs = (songs) => {
    clearResults();
    songs.forEach((song) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${song.name}</strong> by ${song.artist} - <a href="${song.url}" target="_blank">Listen</a>`;
      results.appendChild(li);
    });
  };

  // 검색 버튼 클릭 시 실행되는 함수
  const handleSearch = async () => {
    const artist = artistInput.value.trim();
    clearResults();
    clearError();

    if (!artist) {
      displayError("Please enter an artist name.");
      return;
    }

    const songs = await fetchSongs(artist);
    if (songs.length > 0) {
      displaySongs(songs); // 모든 곡 표시
    }
  };

  // 랜덤 버튼 클릭 시 실행되는 함수
  const handleRandom = async () => {
    const artist = artistInput.value.trim();
    clearResults();
    clearError();

    if (!artist) {
      displayError("Please enter an artist name.");
      return;
    }

    const songs = await fetchSongs(artist);
    if (songs.length > 0) {
      const randomSongs = getRandomTracks(songs, 10); // 랜덤 10곡 선택
      displaySongs(randomSongs); // 랜덤 곡 표시
    }
  };

  // 랜덤 곡 선택 함수
  const getRandomTracks = (tracks, count) => {
    const shuffled = tracks.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count); // 랜덤 10곡 반환
  };

  // 검색 버튼 클릭 이벤트 리스너
  searchButton.addEventListener("click", handleSearch);

  // 랜덤 버튼 클릭 이벤트 리스너
  randomButton.addEventListener("click", handleRandom);

  // Enter 키 입력 시 검색 실행
  artistInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSearch();
    }
  });
});