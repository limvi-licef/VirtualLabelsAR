
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
    //#######################################################################################################################
    //#######################################################################################################################
    // Save content to file
    public static void Save(string path, string content)
    {

        if (!File.Exists(Application.dataPath + "/" + path))
        {
            using (StreamWriter sw = File.CreateText(Application.dataPath + "/" + path))
            {
                sw.WriteLine(content);
            }
        }
        else
        {
            using (StreamWriter sw = File.AppendText(Application.dataPath + "/" + path))
            {
                sw.WriteLine(content);
            }
        }
    }

    //#######################################################################################################################
    //#######################################################################################################################
    // Read string coordinates from save file
    // Return Vector4 coordinates
    public static List<Vector4> ReadVec3(string path)
    {
        List<Vector4> Output_coords;
        List<string> Input_Coords;

        Output_coords = new List<Vector4>();
        Input_Coords = new List<string>();

        using (StreamReader sr = File.OpenText(Application.dataPath + "/" + path))
        {
            string s;
            while ((s = sr.ReadLine()) != null)
            {
                Input_Coords.Add(s);
            }

            foreach (String line in Input_Coords)
            {
                Debug.Log(line);
                Output_coords.Add(StringToVector4(line));
            }
            return Output_coords;
        }
    }

    //#######################################################################################################################
    //#######################################################################################################################
    // Convert string to vector
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

        // store as a Vector3
        Vector4 result = new Vector4(
            float.Parse(sArray[0], NumberStyles.Any, ci),
            float.Parse(sArray[1], NumberStyles.Any, ci),
            float.Parse(sArray[2], NumberStyles.Any, ci),
            float.Parse("1.0", NumberStyles.Any, ci));

        return result;
    }
}
