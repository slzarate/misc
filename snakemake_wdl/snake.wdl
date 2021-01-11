version 1.0

workflow hello_world {
    input {
        File snakemakeFile
        File nameFile
    }

    call say_name {
        input:
            snakemakeFile = snakemakeFile,
            nameFile = nameFile
    }

    output {
        File greeting = say_name.greeting
    }
}

task say_name {
    input {
        File snakemakeFile
        File nameFile
    }

    String snakemakeName = "~{basename(snakemakeFile)}"
    String inputName = "~{basename(nameFile)}"

    command <<<
        snake_base="~{snakemakeName}"
        name_base="~{inputName}"

        cp "~{snakemakeFile}" .
        cp "~{nameFile}" .

        sed -i "s/INPUTFILENAME/${name_base}/g" ./"${snake_base}"
        snakemake --cores
    >>>

    runtime {
        docker : "snakemake/snakemake"
    }

    output {
        File greeting = "greeting.txt"
    }
}