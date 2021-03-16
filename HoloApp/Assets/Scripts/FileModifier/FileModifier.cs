
/*! 
 *  \author Dylan Mielot
 *  \date 12/08/2020
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using Microsoft.MixedReality.Toolkit;
using System.Globalization;

public class FileModifier
{
    /*!
     * \brief Save a content in a file
     * 
     * This method save content in a file. Specify path file and the content to save. The method
     * create the file if not exists, and append text in file if exists.
     * 
     * \param path Save path file.
     * \param content Content to save.
     */
    public static void Save(string path, string content)
    {
        // If path file not exists, create file and write content.
        if (!File.Exists(Application.dataPath + "/" + path))
        {
            using (StreamWriter sw = File.CreateText(Application.dataPath + "/" + path))
            {
                sw.WriteLine(content);
            }
        }
        // If file exists, append text in the file.
        else
        {
            using (StreamWriter sw = File.AppendText(Application.dataPath + "/" + path))
            {
                sw.WriteLine(content);
            }
        }
    }

    /*!
     * \brief Read string coordinates and return a list of vector4.
     * 
     * Read each line of the file, and add them to a list of string Then, convert each line of the list to a vector4 and add them
     * to a list of vector4, this list is returned.
     * 
     * \param path file path to read
     * \return Vector4 list
     */
    public static List<Vector4> ReadVec3(string path)
    {
        List<Vector4> Output_coords;
        List<string> Input_Coords;

        Output_coords = new List<Vector4>();
        Input_Coords = new List<string>();

        using (StreamReader sr = File.OpenText(Application.dataPath + "/" + path))
        {
            string s;
            // Add each line to the list of string.
            while ((s = sr.ReadLine()) != null)
            {
                Input_Coords.Add(s);
            }

            //Convert each line to a vector4 and add them to the list of vector4.
            foreach (String line in Input_Coords)
            {
                Output_coords.Add(StringToVector4(line));
            }
            return Output_coords;
        }
    }

    /*!
     * \brief convert string to a vertor4
     * 
     * \param sVector String vector to convert.
     * \return Vector4.
     */
    public static Vector4 StringToVector4(string sVector)
    {
        // Remove the parentheses
        if (sVector.StartsWith("(") && sVector.EndsWith(")"))
        {
            sVector = sVector.Substring(1, sVector.Length - 2);
        }

        CultureInfo ci = (CultureInfo)CultureInfo.CurrentCulture.Clone();
        ci.NumberFormat.CurrencyDecimalSeparator = ".";

        // split the items
        string[] sArray = sVector.Split(',');

        // store as a Vector4
        Vector4 result = new Vector4(
            float.Parse(sArray[0], NumberStyles.Any, ci),
            float.Parse(sArray[1], NumberStyles.Any, ci),
            float.Parse(sArray[2], NumberStyles.Any, ci),
            float.Parse("1.0", NumberStyles.Any, ci));

        return result;
    }
}
