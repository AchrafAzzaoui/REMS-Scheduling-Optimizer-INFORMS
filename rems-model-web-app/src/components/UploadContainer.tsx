import { useEffect } from "react";
import { useState } from "react";
import axios from "axios";
import apiClient from "../services/axios";
import useDrivePicker from "react-google-drive-picker";
import { Stepper } from "react-form-stepper";
import { FaGoogleDrive } from "react-icons/fa6";

// type for what we send to the backend to parse the google sheet
type SpreadsheetData = {
  fileId: String | undefined;
};

export default function UploadContainer() {
  const [openPicker, authResponse] = useDrivePicker();
  const [currentFileId, setCurrentFileId] = useState<String | undefined>();
  const [authAccessToken, setAuthAccessToken] = useState<String | undefined>();

  // axios instance that interfaces with the fast api backend server
  const api = apiClient;

  // access token is updated asynchronously, so we leave the logic of updating the file id in the
  // callback function because it relies on the data parameter, but we can use useEffect to automatically
  // update the authaccesstoken asychronously based on the authResponse returned by useDrivePicker().

  useEffect(() => {
    if (authResponse?.access_token) {
      const newAuthAccessToken: String | undefined = authResponse.access_token;
      setAuthAccessToken((prevAuthAccessToken) => newAuthAccessToken);
    }
  }, [authResponse]);

  // send both fileId and access token to backend once both are available
  useEffect(() => {
    const sendSpreadsheetData = async () => {
      const spreadsheetData: SpreadsheetData = {
        fileId: currentFileId,
      };
      const response = await api.post("/schedules", spreadsheetData, {
        headers: {
          Authorization: `Bearer ${authAccessToken}`,
        },
      });

      console.log(spreadsheetData);
      console.log(response);
    };
    if (currentFileId && authAccessToken) {
      sendSpreadsheetData();
    }
  }, [currentFileId, authAccessToken]);

  const handleOpenPicker = () => {
    openPicker({
      clientId: import.meta.env.VITE_CLIENT_ID,
      developerKey: import.meta.env.VITE_DEVELOPER_KEY,
      showUploadView: true,
      showUploadFolders: true,
      supportDrives: true,
      multiselect: false,
      callbackFunction: (data) => {
        console.log(data);
        if (data.action === "picked") {
          if (data.docs && data.docs.length > 0) {
            const currentFileId: String = data.docs[0]["id"];
            const currentAuthAccessToken: String | undefined =
              authResponse?.access_token;
            setCurrentFileId((prevCurrentFileId) => currentFileId);
          }
        }
      },
    });
  };

  return (
    <>
      <div className="max-w-3xl md: max-w mx-auto px-4 sm:px-6 lg:px-24 mt-16 bg-white rounded-lg shadow-md py-12 flex flex-col justify-between gap-4">
        <h2 className="text-3xl font-bold">Automated Shift Scheduler</h2>
        <p className="text-xl ">
          Upload your CSV google form responses, and we'll generate an optimized
          schedule for next month.
        </p>
        {/* i */}
        <Stepper
          steps={[
            { label: "Sign in with OAuth" },
            { label: "Upload CSV" },
            { label: "View Generated Schedule" },
          ]}
          activeStep={1}
          styleConfig={{
            completedBgColor: "#9ca3af",
            inactiveBgColor: "#9ca3af",
            activeBgColor: "#064e3b",
          }}
        />
        <div
          onClick={() => handleOpenPicker()}
          className="px-5 py-2.5 border-dotted border-2 border-gray-500 rounded-sm w-full min-h-[200px] flex items-center justify-center"
        >
          <button className="w-5/12 flex flex-col gap-4">
            <FaGoogleDrive className="mx-auto my-auto text-xl" />
            <p>Import from Google Drive</p>
          </button>
        </div>
      </div>
    </>
  );
}
