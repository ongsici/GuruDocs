/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useRef, useState } from "react";

const DEFAULT_HEADERS = {
  "Content-Type": "application/json",
};

export function useFetch(url, method, headers) {
  const [data, setData] = useState();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const fetchCount = useRef(0);
  const [body, setBody] = useState();
  const [success, setSuccess] = useState(false);
  const [queryParams, setQueryParams] = useState();

  const renderFetch = (payload, query) => {
    if (payload) setBody(JSON.stringify(payload));
    setQueryParams(query || undefined);

    fetchCount.current += 1;
  };

  const clearError = () => setError(null);

  useEffect(() => {
    (async () => {
      if (fetchCount.current === 0) return false;
      setSuccess(false);
      setLoading(true);
      return true;
    })();
  }, [fetchCount.current]);

  useEffect(() => {
    (async () => {
      if (!loading) return false;
      try {
        setData(undefined);
        setError(null);
        const delimiter = url.includes("?") ? "&" : "?";
        const urlQueryParams = queryParams
          ? `${delimiter}${new URLSearchParams(queryParams)}`
          : "";
        const response = await fetch(`${url}${urlQueryParams}`, {
          method,
          body: method === "GET" ? undefined : body,
          headers: {
            ...DEFAULT_HEADERS,
            ...headers,
          },
          credentials: "include",
        });
        setSuccess(response?.ok);
        if (response?.ok) {
          if (response?.status === 200) {
            const responseData = await response?.json();
            setData(responseData);
          }
        } else {
          const errorText = await response?.text();
          throw new Error(errorText);
        }
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
        setBody(undefined);
      }
      return true;
    })();
  }, [loading]);

  return { data, error, loading, fetchCount, renderFetch, clearError, success };
}
