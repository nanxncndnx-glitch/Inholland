import streamlit as st
import cv2
import tempfile
import os
from inference_sdk import InferenceHTTPClient
import numpy as np
from PIL import Image
import time
from datetime import datetime
import pandas as pd

import os.path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("Api_Key")


def Model():
    # Title
    st.title("Exercise Detection Beta Version")
    st.markdown("Test the Workout Pose Detection model with your video")

    # Settings section at the top
    st.header("Settings")
    col1, col2, col3 = st.columns(3)

    with col1:
        api_key = st.text_input("Roboflow API Key", type="password", help="Get your API key from roboflow.com")

    with col2:
        frame_skip = st.slider("Process every Nth frame", 1, 30, 10, 
                            help="Higher = faster processing, uses fewer API calls")

    with col3:
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

    st.info(f"📊 Frame skip: {frame_skip} means processing ~{int(30/frame_skip)} frames per second")

    st.markdown("---")

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📹 Upload Video")
        uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov', 'avi', 'mkv'])
        
        if uploaded_file:
            # Save uploaded file temporarily
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            video_path = tfile.name
            
            # Display video
            st.video(video_path)
            
            # Video info
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            duration = total_frames / fps
            cap.release()
            
            st.info(f"📊 Video Info: {total_frames} frames, {fps} FPS, {duration:.1f}s duration")
            st.info(f"🔍 Will process ~{total_frames // frame_skip} frames")

    with col2:
        st.subheader("🎯 Detection Results")
        results_placeholder = st.empty()
        
    # Process button
    if uploaded_file and api_key:
        if st.button("🚀 Start Detection", type="primary", use_container_width=True):
            
            # Initialize Roboflow client
            try:
                CLIENT = InferenceHTTPClient(
                    api_url="https://serverless.roboflow.com",
                    api_key=API_KEY
                )
                
                # Model ID for workout pose detection
                MODEL_ID = "exercise-classification-agacq/7"
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Open video
                cap = cv2.VideoCapture(video_path)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                # Storage for results
                detections = []
                frame_count = 0
                processed_count = 0
                
                # Create columns for real-time display
                col_img, col_data = st.columns([1, 1])
                frame_placeholder = col_img.empty()
                data_placeholder = col_data.empty()
                
                # Process video
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Process every Nth frame
                    if frame_count % frame_skip == 0:
                        # Save frame temporarily
                        temp_frame_path = f"temp_frame_{frame_count}.jpg"
                        cv2.imwrite(temp_frame_path, frame)
                        
                        try:
                            # Run inference
                            result = CLIENT.infer(temp_frame_path, model_id=MODEL_ID)
                            
                            # Parse results
                            if 'predictions' in result and len(result['predictions']) > 0:
                                for pred in result['predictions']:
                                    if pred['confidence'] >= confidence_threshold:
                                        detections.append({
                                            'frame': frame_count,
                                            'time': frame_count / fps,
                                            'exercise': pred['class'],
                                            'confidence': pred['confidence']
                                        })
                                        
                                        # Draw on frame
                                        x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
                                        x1 = int(x - w/2)
                                        y1 = int(y - h/2)
                                        x2 = int(x + w/2)
                                        y2 = int(y + h/2)
                                        
                                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                        label = f"{pred['class']}: {pred['confidence']:.2f}"
                                        cv2.putText(frame, label, (x1, y1-10), 
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            
                            # Display current frame
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame_placeholder.image(frame_rgb, caption=f"Frame {frame_count}", use_container_width=True)
                            
                            # Show latest detection
                            if detections:
                                latest = detections[-1]
                                data_placeholder.metric(
                                    "Latest Detection",
                                    latest['exercise'],
                                    f"{latest['confidence']:.1%} confidence"
                                )
                            
                            processed_count += 1
                            
                        except Exception as e:
                            st.warning(f"Error processing frame {frame_count}: {str(e)}")
                        
                        finally:
                            # Clean up temp frame
                            if os.path.exists(temp_frame_path):
                                os.remove(temp_frame_path)
                    
                    frame_count += 1
                    progress = frame_count / total_frames
                    progress_bar.progress(progress)
                    status_text.text(f"Processing: {frame_count}/{total_frames} frames ({processed_count} analyzed)")
                
                cap.release()
                
                # Display final results
                st.success(f"✅ Processing complete! Analyzed {processed_count} frames")
                
                if detections:
                    st.markdown("---")
                    st.subheader("📊 Analysis Results")
                    
                    # Create DataFrame
                    df = pd.DataFrame(detections)
                    
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Detections", len(detections))
                    
                    with col2:
                        unique_exercises = df['exercise'].nunique()
                        st.metric("Unique Exercises", unique_exercises)
                    
                    with col3:
                        avg_confidence = df['confidence'].mean()
                        st.metric("Avg Confidence", f"{avg_confidence:.1%}")
                    
                    with col4:
                        api_calls = processed_count
                        st.metric("API Calls Used", api_calls)
                    
                    # Exercise breakdown
                    st.markdown("### 🏋️ Exercise Breakdown")
                    exercise_counts = df['exercise'].value_counts()
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.bar_chart(exercise_counts)
                    
                    with col2:
                        for exercise, count in exercise_counts.items():
                            percentage = (count / len(detections)) * 100
                            st.write(f"**{exercise}**: {count} detections ({percentage:.1f}%)")
                    
                    # Timeline
                    st.markdown("### ⏱️ Detection Timeline")
                    st.line_chart(df.set_index('time')['confidence'])
                    
                    # Detailed data
                    with st.expander("📋 View Detailed Detection Data"):
                        st.dataframe(df, use_container_width=True)
                        
                        # Download button
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download Results as CSV",
                            csv,
                            "detection_results.csv",
                            "text/csv",
                            key='download-csv'
                        )
                else:
                    st.warning("⚠️ No exercises detected. Try lowering the confidence threshold or using a different video.")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure your API key is correct and you have API credits available.")

    elif uploaded_file and not api_key:
        st.warning("⚠️ Please enter your Roboflow API key")
        st.info("Get your free API key at: https://roboflow.com")

    else:
        st.info("👆 Upload a video to get started!")